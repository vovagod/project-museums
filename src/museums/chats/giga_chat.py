#from gigachat import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat #as LangChainGigaChat
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from museums.config import settings_giga  # type: ignore  [import-untyped]


def main():

    parser = StrOutputParser()
    
    model = GigaChat(
        credentials=settings_giga.AUTHORIZATION_KEY,
        scope=settings_giga.SCOPE,
        model=settings_giga.MODEL,
        verify_ssl_certs=True,
    )
 
    messages = [
        SystemMessage(
            content="Переведи следующее сообщение с русского на английский!"
        ),
        HumanMessage(content="Как дела, ты куда делся?"),
    ]

    #responce = giga.invoke(messages)
    #chain = giga | parser
    #print(chain.invoke(messages))

    system_template = "Переведи следующий текст на {language}:"
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{text}")]
        )

    result = prompt_template.invoke({"language": "английский", "text": "привет"})
    print(f"RESULT: {result.to_messages()}")

    chain = prompt_template | model | parser
    result = chain.invoke({"language": "английский", "text": "привет"})
    print(f"RESULT: {result}")

    '''
    while(True):
        user_input = input("Пользователь: ")
        if user_input == "пока":
            break
        messages.append(HumanMessage(content=user_input))
        print(f"MESSAGES: {messages}")
        res = giga.invoke(user_input)
        #messages.append(res)
        print("GigaChat: ", res) #.choices[0].message.content)
    '''

if __name__ == "__main__":
    main()