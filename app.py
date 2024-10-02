from flask import Flask, request, jsonify, render_template
from config import *

app = Flask(__name__)

# Маршрут для создания новой задачи
@app.route('/tasks', methods=['POST'])
def post_task():
    """Создание новой задачи"""
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    # Валидация входных данных
    if not title or not description:
        return jsonify({"error": "Title and description are required"}), 400

    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"error": "Could not connect to database"}), 500

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description) VALUES (%s, %s) RETURNING id;",
            (title, description)
        )
        task_id = cursor.fetchone()[0]
        connection.commit()
        return jsonify({"status": "success", "task_id": task_id}), 201
    except Exception as e:
        if connection:
            connection.rollback()
        print("Error while working with PostgreSQL:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Маршрут для обновления задачи
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def put_task(task_id):
    """Обновление задачи"""
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    is_completed = data.get('is_completed')

    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"error": "Could not connect to database"}), 500

        cursor = connection.cursor()
        query = "UPDATE tasks SET "
        query_params = []

        if title:
            query += "title = %s, "
            query_params.append(title)
        if description:
            query += "description = %s, "
            query_params.append(description)
        if is_completed is not None:
            query += "is_completed = %s, "
            query_params.append(is_completed)

        # Убираем последнюю запятую
        query = query.rstrip(', ')
        query += " WHERE id = %s"
        query_params.append(task_id)

        cursor.execute(query, tuple(query_params))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

        return jsonify({"status": "success"}), 200
    except Exception as e:
        if connection:
            connection.rollback()
        print("Error while working with PostgreSQL:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Маршрут для получения всех задач
@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Получение всех задач"""
    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"error": "Could not connect to database"}), 500

        cursor = connection.cursor()
        cursor.execute("SELECT id, title, description, is_completed FROM tasks LIMIT 100;")
        tasks = cursor.fetchall()

        task_list = [{"id": task[0], "title": task[1], "description": task[2], "is_completed": task[3]} for task in tasks]
        return jsonify(task_list), 200
    except Exception as e:
        print("Error while working with PostgreSQL:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Маршрут для удаления задачи
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Удаление задачи"""
    try:
        connection = get_connection()
        if connection is None:
            return jsonify({"error": "Could not connect to database"}), 500

        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

        connection.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        if connection:
            connection.rollback()
        print("Error while working with PostgreSQL:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Маршрут для главной страницы с интерфейсом
@app.route('/')
def index():
    return render_template('index.html')

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)

