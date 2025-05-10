import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button
from PIL import Image, ImageTk
import nltk
from nltk.chat.util import Chat, reflections

# Define chatbot responses and patterns
pairs = [
    [
        r"my name is (.)",
        ["Hello %1, how can I assist you with your college-related inquiries today?"]
    ],
    [
        r"hi|hey|hello|hlo",
        ["Hello! How can I help you with your college-related questions?"]
    ],
    [
        r"what is your name?",
        ["You can call me deep . How can I assist you with your college needs today?"]
    ],
    [
        r"how are you ?",
        ["I'm an AI-powered CollegeBot, programmed to assist students and parents like you. How can I help you today with your college-related concerns?"]
    ],
    [
        r"sorry?",
        ["No problem. How can I assist you further?"]
    ],
    [
        r"college application|college admissions|college admission|admissions|admission",
        ["To apply to college or get information about the admission process, please provide some of your details and for further you can contact with us."]
    ],
    [
        r"academics|academic support",
        ["For academic support, you can reach out to our college's academic advising office or tutoring center. They can assist you with course selection, study strategies, and academic resources."],
    ],
    [
        
        r"courses offered|available programs",
        ["To find information about the courses offered and available programs at your college, please visit the college's official website or contact the college's academic department."],
    ],
    [
        r"cultural programs|events",
        ["To learn about cultural programs, events, or clubs at our college, check the college's event calendar, or consider joining cultural or student organizations on campus for a diverse experience."],
    ],
    [
        r"scholarships|financial aid",
        ["If you're looking for scholarships or financial aid options, please let me know your area of interest or the specific type of scholarship you're looking for, and I'll provide you with relevant information."]
    ],
    [
        r"campus facilities|campus|hostel",
        ["The campus facilities at many colleges include libraries, sports facilities, computer labs, and more. You can visit the college's website or contact the campus administration for detailed information about the facilities available on your campus."],
    ],
    [
        r"student housing|dormitories|student hostel ",
        ["To inquire about student housing or dormitories, you can contact the college's housing office or visit their website for information about housing options, rates, and application procedures."],
    ],
    [
        r"extracurricular activities|clubs",
        ["Colleges offer a variety of extracurricular activities and clubs. To get involved, check out the college's student affairs or club directory on their website. You can also attend club fairs during orientation to learn about different options."],
    ],
    [
        r"career services|job placement",
        ["For career services and job placement assistance, contact the college's career center. They can help you with resume building, job searches, internships, and career counseling."],
    ],
    [
        r"tuition fees|financial aid|fees",
        ["To find information about tuition fees and available financial aid options, visit the college's financial aid office or the financial services section on their website. They can provide details on scholarships, grants, and payment plans."],
    ],
    [
        r"faculty|professors",
        ["To learn about the faculty or professors at our college, you can visit the college's website and navigate to the 'Faculty' or 'Departments' section. There, you'll find profiles and contact information for the professors in different departments."],
    ],
    [
        r"courses|majors",
        ["To learn about available courses or majors, please specify your field of interest , and I'll provide you with details about the programs they offer."]
    ],
    [
        r"study tips",
        ["Studying effectively is important. I can provide you with some study tips and strategies. What subject or topic are you currently studying?"]
    ],
    [
        r"quit",
        ["Thank you for using our CollegeBot. If you have any more college-related questions in the future, feel free to ask. Best of luck with your academic journey!"]
    ],
    [
        r"(.)",
        ["I apologize, but I couldn't understand your query. Could you please rephrase or provide more details about your college-related question?"]
    ]
]

# Create the chatbot
chatbot = Chat(pairs, reflections)


#\Create a function to send a user's message to the chatbot
def send_message(event=None):
    user_message = user_input.get()
    response = chatbot.respond(user_message)
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"You: {user_message}\n", "user")
    chat_history.insert(tk.END, f"CollegeBot: {response}\n", "bot")
    chat_history.see(tk.END)
    chat_history.config(state=tk.DISABLED)
    user_input.delete(0, tk.END)
 


# Create the main GUI window
root = tk.Tk()
root.title("CollegeBot")

# Customize the background color and window size
root.configure(bg="#333333")  # Set a dark gray background color
root.geometry("1200x600")     # Set the window size to 1200x600 pixels


# Add a title/header label at the top with custom font and color
title_label = tk.Label(root, text="BRCM College of Engineering and Technology", font=("Arial", 24, "bold"), bg="#F0F0F0", fg="navy")
title_label.pack(pady=10)

# Create a chat history Text widget with custom fonts and colors
chat_history = Text(root, wrap=tk.WORD, state=tk.DISABLED, bg="white", fg="black", font=("Arial", 12))
chat_history.pack(expand=True, fill=tk.BOTH)

# Customize the scrollbar with a matching background color
scrollbar = Scrollbar(chat_history)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_history.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=chat_history.yview)

# Representing chatbot by its name with custom font and color
chatbot_name_label = tk.Label(root, text="The College Chatbot", font=("Arial", 20, "italic"), fg="blue", bg="#F0F0F0")
chatbot_name_label.pack(pady=20)

# Create a user input field with a custom font
user_input = Entry(root, width=70, font=("Arial", 12))
user_input.pack(pady=10)

# Customize the send button with a different background color
send_button = Button(root, text="Send", command=send_message, font=("Arial", 12), bg="green", fg="white")
send_button.pack()

# Add informative text with custom formatting
info_text = """
Welcome to CollegeBot, yo
ur friendly college assistant! I'm here to help you with any college-related questions and concerns.
You can ask me about admissions, academics, programs, campus facilities, scholarships, and much more. Just type your question, and I'll provide you with the information you need.

Feel free to explore and learn about your college journey with me. I'm here to make your experience better!
"""
info_label = tk.Label(root, text=info_text, font=("Arial", 11), justify=tk.CENTER, bg="#F0F0F0")
info_label.pack(pady=20)

# Define styles for user and bot messages with custom colors
chat_history.tag_configure("user", foreground="black")
chat_history.tag_configure("bot", foreground="blue")

# Start the GUI main loop
root.mainloop()