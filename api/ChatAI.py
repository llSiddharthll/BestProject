import g4f

class Gemini:
    def __init__(self):
        self.messages = []

    def chat(self, *args):
        assert args != ()

        message = " ".join(args)
        self.messages.append({"role": "user", "content": message})

        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            provider=g4f.Provider.Gemini,
            messages=self.messages,
            stream=True,
        )
        ms = ""
        for message in response:
            ms += message
        self.messages.append({"role": "assistant", "content": ms.strip()}) # Strip whitespace from the message content
        return ms.strip() # Return the message without trailing whitespace

    @staticmethod
    def chat_cli(message):
        """Generate completion based on the provided message"""
        gemini = Gemini()
        return gemini.chat(message)