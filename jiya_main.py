import tkinter as tk
from tkinter import Button, ttk
import subprocess
import jiya_duplicate
import add_history  # Assuming this module contains fetch_conversations() function
import mysql.connector
from mysql.connector import Error
import jokes

def show(username):

    # Define the function to run the second script
    def run_second_script():
        # Display the "Listening....." message on the label when the button is clicked
        listening_label.config(text="Listening.....")
        
        # Run the jiya_duplicate script
        num = jiya_duplicate.run()
        
        if num == 2:
            listening_label.config(text="Execution Complete | Conversation saved successfully...")

    # Function to fetch conversation history from the database using add_history.fetch_conversations()
    def display_conversations():
        conversations = add_history.fetch_conversations()  # Get conversations from the database
        
        # Create a new window to display conversation history
        history_window = tk.Toplevel(root)
        history_window.title("Conversation History")
        history_window.geometry("800x400")

        # Create a Treeview widget with 4 columns: ID, User Input, Assistant Response, Timestamp
        tree = ttk.Treeview(history_window, columns=("ID", "User Input", "Assistant Response", "Timestamp"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("User Input", text="User Input")
        tree.heading("Assistant Response", text="Assistant Response")
        tree.heading("Timestamp", text="Timestamp")

        # Insert conversation records into the Treeview
        for conversation in conversations:
            tree.insert("", tk.END, values=conversation)

        # Add a vertical scrollbar to the Treeview widget
        scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Pack the Treeview widget
        tree.pack(expand=True, fill=tk.BOTH)

    # Function to add tasks to the database
    def addtask(date, tasks):
        # Add Tasks into Base
        connection = None
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="jiya"
            )
            print("Connection to MySQL DB successful")

            cursor = connection.cursor()
            query = "INSERT INTO remember (date, tasks) VALUES (%s, %s)"
            values = (date, tasks)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()

            return "Work Done"

        except Error as e:
            print(f"The error '{e}' occurred")
            return "Error"

    # Function to show the add task form
    def show_add_task_form():
        # Create a new window for adding tasks
        add_task_window = tk.Toplevel(root)
        add_task_window.title("Add New Task")
        add_task_window.geometry("400x300")

        # Create and pack the label for date
        date_label = tk.Label(add_task_window, text="Date (YYYY-MM-DD):")
        date_label.pack(pady=5)
        date_entry = tk.Entry(add_task_window)
        date_entry.pack(pady=5)

        # Create and pack the label for task
        task_label = tk.Label(add_task_window, text="Task Description:")
        task_label.pack(pady=5)
        task_entry = tk.Entry(add_task_window)
        task_entry.pack(pady=5)

        # Function to handle task submission
        def submit_task():
            date = date_entry.get()
            task = task_entry.get()
            if date and task:
                result = addtask(date, task)
                result_label.config(text=result)
            else:
                result_label.config(text="Please fill in both fields.")

        # Button to submit task
        submit_button = tk.Button(add_task_window, text="Add Task", command=submit_task)
        submit_button.pack(pady=10)

        # Result label for feedback
        result_label = tk.Label(add_task_window, text="")
        result_label.pack(pady=5)

    # Function to insert a joke into the MySQL database
    def insert_joke(joke):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="jiya"
            )
            cursor = connection.cursor()
            query = "INSERT INTO jokes (joke) VALUES (%s)"
            cursor.execute(query, (joke,))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Joke added successfully!")
        except Error as e:
            print(f"The error '{e}' occurred")
            messagebox.showerror("Error", "There was an error adding the joke.")

    # Function to show the add joke form
    def show_add_joke_form():
        # Create a new window for adding jokes
        add_joke_window = tk.Toplevel(root)
        add_joke_window.title("Add New Joke")
        add_joke_window.geometry("400x300")

        # Create and pack the label for joke
        joke_label = tk.Label(add_joke_window, text="Enter your joke:")
        joke_label.pack(pady=5)
        joke_entry = tk.Entry(add_joke_window, width=40)
        joke_entry.pack(pady=5)

        # Function to handle joke submission
        def submit_joke():
            joke = joke_entry.get()
            if joke:
                result=jokes.insert_joke(joke)
                joke_entry.delete(0, tk.END)  # Clear the input field
                result_label.config(text=result)
            else:
                result_label.config(text="Please fill fields.")

        # Button to submit joke
        submit_button = tk.Button(add_joke_window, text="Add Joke", command=submit_joke)
        submit_button.pack(pady=10)

        # Result label for feedback
        result_label = tk.Label(add_joke_window, text="")
        result_label.pack(pady=5)

    def insert_qa(question, answer):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="jiya")
            cursor = connection.cursor()
            query = "INSERT INTO qa_data (question, answer) VALUES (%s, %s)"
            cursor.execute(query, (question, answer))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Question-Answer added successfully!")
        except Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_add_qa_form():
        add_qa_window = tk.Toplevel(root)
        add_qa_window.title("Add Question-Answer")
        add_qa_window.geometry("400x300")
        tk.Label(add_qa_window, text="Enter Question:").pack(pady=5)
        question_entry = tk.Entry(add_qa_window, width=40)
        question_entry.pack(pady=5)
        tk.Label(add_qa_window, text="Enter Answer:").pack(pady=5)
        answer_entry = tk.Entry(add_qa_window, width=40)
        answer_entry.pack(pady=5)
        def submit_qa():
            question = question_entry.get()
            answer = answer_entry.get()
            if question and answer:
                insert_qa(question, answer)
                question_entry.delete(0, tk.END)
                answer_entry.delete(0, tk.END)
                result_label.config(text="Question-Answer added!")
            else:
                result_label.config(text="Please fill in both fields.")
        tk.Button(add_qa_window, text="Add Q&A", command=submit_qa).pack(pady=10)
        result_label = tk.Label(add_qa_window, text="")
        result_label.pack(pady=5)

    # GUI code
    # Create the main application window
    root = tk.Tk()
    root.title("J.I.Y.A - The Personal Voice Assistant")
    root.geometry("600x400")  # Set the window size

    # Create a frame for the top label with a background color
    top_frame = tk.Frame(root)
    top_frame.pack(pady=10)  # Add some vertical padding

    # Display Username on the Right Side
    username_label = tk.Label(root, text=f"Logged in as: {username}", font=("Helvetica", 12), bg="white", fg="black")
    username_label.pack(padx=10, pady=10)  # Position on right side

    # Create and pack the top label
    top_label = tk.Label(top_frame, text="J.I.Y.A - The Personal Voice Assistance", font=("Helvetica", 16), bg="lightgray")
    top_label.pack()

    # Create a frame for the sidebar
    sidebar_frame = tk.Frame(root, width=200, bg="lightgray")
    sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

    # Create buttons in the sidebar
    button1 = tk.Button(sidebar_frame, text="Execute", command=run_second_script)  # Call the function here
    button1.pack(pady=10)

    # Button 2 to add jokes
    button2 = tk.Button(sidebar_frame, text="Add Joke", command=show_add_joke_form)  # Show conversation history
    button2.pack(pady=10)

    # Button to add new task
    button3 = tk.Button(sidebar_frame, text="Add Task", command=show_add_task_form)  # Open add task form
    button3.pack(pady=10)

    # Button to add Q&A
    button4 = tk.Button(sidebar_frame, text="Add Q&A", command=show_add_qa_form)  # Open add Q&A form
    button4.pack(pady=10)

    # Button to display history
    button5 = tk.Button(sidebar_frame, text="History", command=display_conversations)  # Open add joke form
    button5.pack(pady=10)

    # Create a content frame in the middle area
    content_frame = tk.Frame(root)
    content_frame.pack(expand=True, fill=tk.BOTH)

    # Create a video player object in the content frame
    #video_player = TkinterVideo(master=content_frame, scaled=True)
   # video_player.pack(expand=True, fill="both")

    # Create a label in the content frame to display "Listening....."
    listening_label = tk.Label(content_frame, text="", font=("Helvetica", 14), bg="lightgray")
    listening_label.pack(pady=10)

    # Create labels for bottom-left and bottom-right corners
    bottom_left_label = tk.Label(root, text="DM | Enterprise", font=("Helvetica", 10))
    bottom_left_label.pack(side=tk.LEFT, anchor=tk.SW, padx=10, pady=10)  # Bottom-left corner

    bottom_right_label = tk.Label(root, text="TrueZero", font=("Helvetica", 10))
    bottom_right_label.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)  # Bottom-right corner

    # Start the Tkinter event loop
    root.mainloop()
