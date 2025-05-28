from app import Application


app = Application().add_extensions().build()

if __name__ == "__main__":
    app.run()
