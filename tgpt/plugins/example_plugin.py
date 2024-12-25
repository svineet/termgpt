class Plugin:
    tag = "@example"

    def run(self, input_text, context):
        return f"Example plugin processed: {input_text}"
