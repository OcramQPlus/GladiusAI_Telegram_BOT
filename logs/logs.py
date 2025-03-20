import os

def logs(user_id, user_name, message):
    # Для пользователя
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True) 
    log_path = os.path.join(log_dir, f"{user_id}.{user_name}.log")
    with open(log_path, "a", encoding="utf-8") as log_file:
        user_data = f"{user_name} ({user_id}):"
        log_file.write(f"{user_data} {message = }\n")
    # Общие логи
    log_path = os.path.join(log_dir, "logs.log")
    with open(log_path, "a", encoding="utf-8") as log_file:
        user_data = f"{user_name} ({user_id}):"
        log_file.write(f"{user_data} {message = }\n")