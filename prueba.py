from datetime import datetimetime

today = datetime.now()
print(today.strftime("%Y_%m_%d_%H_%M_%S_inicio_periodo") + '.png')