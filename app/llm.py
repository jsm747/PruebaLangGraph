"""Server-side chat configuration. Credentials never enter browser responses."""
from dataclasses import dataclass, field
import math
import os
from urllib.parse import urlparse, parse_qs
import httpx


class ChatError(ValueError):
    def __init__(self, message, *, uncertain=False):
        super().__init__(message)
        self.uncertain = uncertain


@dataclass
class ChatConfig:
    provider: str
    endpoint: str
    model: str
    key: str = field(repr=False)
    max_tokens: int = 4096
    effort: str = ''
    token_parameter: str = 'max_completion_tokens'
    input_price: float | None = None
    output_price: float | None = None

    @classmethod
    def read(cls):
        provider = os.environ.get('APF_LLM_PROVIDER', 'compatible' if os.environ.get('APF_LLM_URL') else 'openai')
        if provider not in ('openai','azure','compatible'):
            raise ChatError('APF_LLM_PROVIDER debe ser openai, azure o compatible.')
        endpoint = os.environ.get('APF_LLM_URL', 'https://api.openai.com/v1/chat/completions' if provider == 'openai' else '')
        parsed = urlparse(endpoint)
        if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
            raise ChatError('Configura APF_LLM_URL con la URL HTTPS completa del endpoint de chat.')
        if any(k.lower() in ('key','api-key','api_key','token','access_token') for k in parse_qs(parsed.query)):
            raise ChatError('La credencial debe estar en un secreto de Codespaces, no en la URL.')
        model = os.environ.get('APF_LLM_MODEL','').strip()
        key = os.environ.get('APF_LLM_API_KEY','').strip()
        if not model or not key:
            raise ChatError('Configura APF_LLM_MODEL y el secreto APF_LLM_API_KEY en el servidor.')
        effort = os.environ.get('APF_LLM_REASONING_EFFORT','')
        if effort not in ('','low','medium','high'):
            raise ChatError('El esfuerzo opcional debe ser low, medium o high.')
        parameter = os.environ.get('APF_LLM_TOKEN_PARAMETER', 'max_tokens' if provider == 'compatible' else 'max_completion_tokens')
        if parameter not in ('max_tokens','max_completion_tokens'):
            raise ChatError('El parámetro de límite de tokens no es válido.')
        try:
            limit = int(os.environ.get('APF_LLM_MAX_OUTPUT_TOKENS','4096'))
            if not 256 <= limit <= 16384: raise ValueError()
            rates = [os.environ.get(k) for k in ('APF_LLM_INPUT_USD_PER_MILLION','APF_LLM_OUTPUT_USD_PER_MILLION')]
            if any(x is not None for x in rates):
                rates = [float(x) for x in rates]
                if not all(math.isfinite(x) and x >= 0 for x in rates): raise ValueError()
            else: rates = [None,None]
        except (TypeError,ValueError):
            raise ChatError('Revisa el límite de tokens y las dos tarifas opcionales.')
        return cls(provider, endpoint, model, key, limit, effort, parameter, *rates)

    def safe_status(self):
        return {'provider':self.provider,'model':self.model,'effort':self.effort or 'predeterminado',
                'priced':self.input_price is not None,'ready':True}


def status():
    result={'enabled':os.environ.get('APF_BUILDER','guided')=='openai-compatible','ready':False,
            'credential_present':bool(os.environ.get('APF_LLM_API_KEY','').strip())}
    try:
        result.update(ChatConfig.read().safe_status())
    except ChatError as exc:
        result['message']=str(exc)
    return result


def complete_json(messages):
    config=ChatConfig.read()
    body={'model':config.model,'messages':messages,'response_format':{'type':'json_object'},
          config.token_parameter:config.max_tokens}
    if config.effort: body['reasoning_effort']=config.effort
    headers={'api-key':config.key} if config.provider=='azure' else {'Authorization':'Bearer '+config.key}
    try:
        response=httpx.post(config.endpoint,json=body,headers=headers,timeout=90.0)
        if response.status_code in (401,403):
            raise ChatError('El proveedor rechazó la credencial o el acceso al modelo.',uncertain=True)
        if response.status_code==429:
            raise ChatError('El proveedor informa de un límite o cuota agotada. Revisa tu cuenta antes de repetir.',uncertain=True)
        if response.status_code==400:
            raise ChatError('El proveedor no admite la solicitud. Revisa el modelo, el endpoint y sus parámetros.',uncertain=True)
        response.raise_for_status()
        data=response.json()
        content=data['choices'][0]['message']['content']
        if not isinstance(content,str): raise ValueError()
        usage=data.get('usage') or {}
        n_in,n_out=usage.get('prompt_tokens'),usage.get('completion_tokens')
        valid_usage=all(isinstance(n,int) and not isinstance(n,bool) and n>=0 for n in (n_in,n_out))
        cost=(n_in*config.input_price+n_out*config.output_price)/1_000_000 if valid_usage and config.input_price is not None else None
        return content,{'backend':'openai-compatible','provider':config.provider,'model':config.model,
                        'input_tokens':n_in if valid_usage else None,'output_tokens':n_out if valid_usage else None,
                        'cost_usd':cost,'cost_known':cost is not None}
    except ChatError:
        raise
    except (httpx.HTTPError,KeyError,ValueError,TypeError,IndexError) as exc:
        raise ChatError('No se pudo obtener una respuesta utilizable del proveedor. No se reintentará automáticamente; comprueba su consumo antes de repetir.',uncertain=True) from exc
