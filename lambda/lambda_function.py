import logging
import ask_sdk_core.utils as ask_utils
import requests
import json

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Seja bem vindo a Micro Cervejaria Home Beer. O que você gostaria ?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Você pode pedir para iniciar alguma receita, iniciar limpeza, listar as receitas, ou até mesmo detalhar alguma receita  Podendo também indicar o tempo para fim de algum  processo, ou tempo para fim da limpeza"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



class ListarReceitasIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ListarReceitasIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Suas receitas são "

        headers = {'Authorization': 'cervejaria'}
        response = requests.get('https://api-homebeer.herokuapp.com/receitas', headers=headers)
        listaReceitas = response.json()
        for cerveja in listaReceitas:
            speak_output += cerveja["nome"] + ", "
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class IniciarReceitaIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("iniciarReceitaIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        pedido_receita = slots['Receita'].value

        headers = {'Authorization': 'cervejaria'}
        response = requests.get('https://api-homebeer.herokuapp.com/receitas', headers=headers)
        listaReceitas = response.json()
        lista =[]
        for cerveja in listaReceitas:
            lista.append(cerveja["nome"].lower())
        if pedido_receita not in lista:
            speak_output = "Você não possui esta receita em sua Micro cervejaria, se quiser pergunte por sua lista de receitas"
        elif pedido_receita in lista:
            cerveja_inicializar = pedido_receita
            payload={'nomeReceita': cerveja_inicializar}
            response = requests.post('https://api-homebeer.herokuapp.com/iniciar', headers=headers, data=payload)

            re=response.json()

            speak_output = re['message']

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class IniciarLimpezaIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("iniciarLimpezaIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = ""
        slots = handler_input.request_envelope.request.intent.slots
        pedido_resposta = slots['answer'].value

        if pedido_resposta == 'sim':
            headers = {'Authorization': 'cervejaria'}
            response = requests.post('https://api-homebeer.herokuapp.com/limpeza', headers=headers)
            serverResponse = response.json()
            speak_output = serverResponse["message"]
        else:
            speak_output = "limpeza nao iniciada"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class DetalharReceitaIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("detalharReceitaIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        pedido_receita = slots['nomeReceita'].value

        headers = {'Authorization': 'cervejaria'}
        url = 'https://api-homebeer.herokuapp.com/receitas?nome_like=' + pedido_receita
        response = requests.get(url, headers=headers)
        receita = response.json()[0]
        ingredientes = ""
        for i in receita['ingredientes']:
            ingredientes += F"{i['nome']} {i['quantidade']} {i['unidadeMedida']}. "

        brassagem = ""
        for i in receita['brassagem']:
            brassagem +=  F"{i['temperatura']} graus célsius, por {i['tempo']} minutos. "

        fervura = ""
        for i in receita['fervura']['ingredientes']:
            fervura += F"{i['quantidade']} {i['unidadeMedida']} de {i['nome']} serão adicionados aos {i['tempo']} minutos. "

        speak_output = F"""\
        A cerveja {receita['nome']} é uma {receita['descricao']}. \
        Seu tempo médio de produção é de {receita['tempoMedio']} minutos e produz {receita['quantidadeLitros']} litros. \
        Os ingredientes utilizados são: {ingredientes}\
        Durante sua fase de aquecimento, a cerveja é aquecida a uma temperatura de {receita['aquecimento']['temperatura']} graus célsius. \
        Durante a brassagem, será realizado os seguintes degraus de aquecimento:  A temperatura vai ficar em {brassagem} \
        A fervura vai durar um tempo total de {receita['fervura']['tempoTotal']} minutos. E os seguintes ingredientes vão ser adicionados: {fervura}\
        """
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class visualizarProcessotHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("visualizarProcessoIntet")(handler_input)


    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        etapa = slots['processo'].value


        headers = {'Authorization': 'cervejaria'}
        response = requests.get('https://api-homebeer.herokuapp.com/processo/{}'.format(etapa), headers=headers)
        processo = response.json()

        fala_a=''
        fala_b=''

        if etapa== 'brassagem':
            qnt_degrais_temperatura = len(processo['etapas'])
            fala_a = 'No processo de '+etapa+' encontrei '+ str(qnt_degrais_temperatura)+' degrais de temperatura. O mosto será aquecido a uma temperatura de '

            for i in range(len(processo['etapas'])):
                fala_b+= processo['etapas'][i]['temperatura'] +' graus célsius por '+ processo['etapas'][i]['tempo']+' minutos, '
            fala_final=fala_a+ fala_b[:-2]

        elif etapa == 'aquecimento':
            fala_final= 'No processo de '+ etapa + ' o mosto será aquecido a uma temperatura de '+processo['etapas'][0]['temperatura']+' graus célsius.'
        elif etapa == 'fervura':
            fala_a = "No processo de "+ etapa+' é necessário inserir os seguintes ingredientes: '
            for ingrediente in processo['etapas'][0]['ingredientes']:
                fala_b+=ingrediente['quantidade']+' '+ingrediente['unidadeMedida']+' de ' +ingrediente['nome']+' aos '+ingrediente['tempo'] +' minutos, '
            fala_final= fala_a +fala_b[:-2]
        else:
            fala_final= "Não foi encontrado um processo com este nome, os processos disponíveis são: brassagem, aquecimento e fervura."

        speak_output=fala_final
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
class lerTempoRestanteHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("lerTempoRestante")(handler_input)


    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        headers = {'Authorization': 'cervejaria'}
        response = requests.get('https://api-homebeer.herokuapp.com/processo/', headers=headers)
        processo = response.json()
        output = ''
        if processo['processo'] == 'aquecimento':
            output = 'Para o fim do processo faltam ' +processo['tempoRestante']+' minutos. O mosto deve ser aquecido a '+processo['etapas'][0]['temperatura']+' graus. E no momento a temperatura atinge '+processo['temperaturaAtual']+' graus'
        elif processo['processo'] == 'brassagem':
            output = 'Para o fim do processo faltam ' +processo['tempoRestante']+' minutos. O mosto deve ser aquecido a '+processo['etapas'][1]['temperatura']+' graus. E no momento a temperatura atinge '+processo['temperaturaAtual']+' graus'
        elif processo['processo'] == 'fervura':
            output = 'Para o fim do processo faltam ' +processo['tempoRestante']+' minutos. Certifique-se que adicionou ' 
            for ingrediente in processo['etapas'][0]['ingredientes']:
                speak_output += ingrediente['quantidade']+ ' gramas de ' +ingrediente['nome']+ ' no tempo de ' +ingrediente['tempo']+ ' Minutos. '
        else:
            output = 'Nenhum Processo em andamento'
            
        speak_output = output
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Adeus!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Desculpe, Eu tive um problema com o que você falou. Por favor, tente de novo."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ListarReceitasIntentHandler())
sb.add_request_handler(IniciarLimpezaIntentHandler())
sb.add_request_handler(visualizarProcessotHandler())
sb.add_request_handler(IniciarReceitaIntentHandler())
sb.add_request_handler(DetalharReceitaIntentHandler())
sb.add_request_handler(lerTempoRestanteHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
