from src import Config, Window

conf = Config("configs/app.json")
w = Window.initiate_fom_config(conf)
w.open()