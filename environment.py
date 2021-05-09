class Environment:
    LOCAL_DB = 'mongodb://localhost:27017/baymaxx'
    REMOTE_DB = 'mongodb+srv://admin:lugHep3DzkVKmX3j@cluster0.kamtz.mongodb.net/Baymaxx?retryWrites=true&w=majority'
    FLASK_SERVER = 'http://localhost:5000/'
    EXPRESS_SERVER = 'http://localhost:8500/'
    WEB_PORTAL = 'http://localhost:4200/'
    RASA_CHATBOT_SERVER = 'http://localhost:5005/'
    RASA_ACTION_SERVER = 'http://localhost:5055/'

    RASA_CHATBOT_WEBHOOK = 'http://localhost:5005/webhooks/rest/webhook'
    RASA_ACTION_WEBHOOK = "http://localhost:5055/webhook"
