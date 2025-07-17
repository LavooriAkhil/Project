from django.shortcuts import render, redirect  # Add redirect here
from django.urls import reverse  # Import reverse for URL reversing
import os
import json

# Load questions from JSON file
file_path = os.path.join(os.path.dirname(__file__), "questions.json")
with open(file_path, "r", encoding="utf-8") as file:
    j = json.load(file)
    d = [
        'images/webdev.png',
        'images/app_development.jpg',
        'images/Full_Stack.png',
        'images/al.png',
        'images/data_science.jpg',
        'images/cloud.jpg'
    ]
    images = {}
    c = 0
    for i in j.keys():
        images[i] = d[c]
        c += 1

def login(request):
    if request.method == 'GET':
        # Check if it's a login or signup request
        if 'username' in request.GET and 'password' in request.GET:
            # Login logic
            username = request.GET.get('username')
            password = request.GET.get('password')
            # Add your authentication logic here
            # For now, just redirect to the homepage
            return redirect(reverse('homepage'))
        elif 'username' in request.GET and 'email' in request.GET and 'password1' in request.GET and 'password2' in request.GET:
            # Signup logic
            username = request.GET.get('username')
            email = request.GET.get('email')
            password1 = request.GET.get('password1')
            password2 = request.GET.get('password2')
            
            # Validate passwords
            if password1 == password2:
                # Add your user creation logic here
                # For now, redirect to the homepage
                return redirect(reverse('homepage'))
            else:
                # Handle password mismatch error
                return redirect(reverse('loginpage'))
    return render(request, 'login.html')
def homepage(request):
    data = {
        'courses': images
    }
    return render(request, 'index.html', {'data': data})

def course(request):
    course = request.GET.get('course_')
    course_iframe = {}
    print(course)
    course_list = [
        '<iframe width="560" height="315" src="https://www.youtube.com/embed/dX8396ZmSPk?si=BMXhvtjU67AXrSVn" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',
        '<iframe width="560" height="315" src="https://www.youtube.com/embed/7nQsQ0rvYqQ?si=9SmExWcjSgDT7xRG" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',
        '<iframe width="560" height="315" src="https://www.youtube.com/embed/5PdEmeopJVQ?si=7f6IM4UnNC8ZmCVG" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',
        '<iframe width="560" height="315" src="https://www.youtube.com/embed/7O60HOZRLng?si=E_aj3Uh0oot-DP9F" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',
        '<iframe width="560" height="315" src="https://www.youtube.com/embed/KxryzSO1Fjs?si=7CDoiqRfEIDk0ChL" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',
        '<iframe width="560" height="315" src="https://www.youtube.com/embed/RWgW-CgdIk0?si=dRnnQ6i0XDfHfCpH" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
        '<iframe width="560" height="315" src="https://www.youtube.com/embed/rwF-X5STYks?si=dDf-Lip05KJZxwHt" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
    
    ]
    c = 0
    SUMMARY=["The Web Development course offers a comprehensive guide to building modern websites and web applications, covering both front-end and back-end technologies. It begins with HTML, teaching how to structure web pages using elements like headings, paragraphs, links, images, and forms. Next, CSS is introduced for styling, focusing on layout, color, typography, and responsive design using Flexbox and Grid. JavaScript is then covered to add interactivity and dynamic behavior to web pages, including concepts like variables, functions, events, and manipulating the Document Object Model (DOM). The course then advances to modern front-end development with frameworks like React.js, explaining the use of components, props, state, and hooks to build single-page applications. On the back-end side, students learn Node.js and Express.js to handle server-side logic, build RESTful APIs, and manage user authentication and data operations. It also introduces MongoDB, a NoSQL database, for storing and retrieving data efficiently. Alongside coding, the course emphasizes essential tools like Git and GitHub for version control, and deployment platforms such as Netlify and Render for publishing live web apps. Learners build hands-on projects including personal portfolios, to-do lists, and full-stack applications to apply what they learned in real-world scenarios. Throughout the course, best practices in clean code, debugging, documentation, and team collaboration are stressed, preparing students for professional development environments. By the end of the course, learners will have a solid foundation in web development and the ability to independently create responsive, dynamic, and data-driven websites. Whether pursuing a career in front-end, back-end, or full-stack development, this course equips individuals with the knowledge and confidence to build complete web solutions from scratch using industry-standard technologies.The course introduces the basics of building static websites. It covers HTML for structuring content using elements like headings, paragraphs, images, links, and forms. CSS is taught for styling, focusing on properties like color, layout, and typography. Learners explore the box model, positioning, Flexbox, and Grid for responsive design .",
    "The Roadmap of Web Development course outlines the step-by-step journey to become a full-stack web developer. It begins with learning HTML, CSS, and JavaScript for front-end development, followed by advanced topics like responsive design, Git/GitHub, and frameworks like React. The back-end section introduces Node.js, Express, and databases like MongoDB or PostgreSQL. Students also learn REST APIs, authentication, deployment, and DevOps basics. The course emphasizes real-world projects, version control, and best coding practices. It's ideal for beginners aiming to understand the entire web development process, from static sites to dynamic full-stack applications.",
    "This Full Stack Development course teaches how to build modern web applications using React.js for the front-end, Spring Boot (Java) for the back-end, and MongoDB as the database. It starts with creating responsive UIs using React, managing state, and integrating APIs. On the back-end, it covers building RESTful APIs with Spring Boot, implementing business logic, and handling security and authentication. MongoDB is used for storing and querying data in a flexible, NoSQL format. The course emphasizes full-stack integration, deployment, and project-based learning, making it ideal for aspiring developers aiming to build scalable, end-to-end web applications .",
    "The Artificial Intelligence with Python tutorial introduces the fundamentals of AI and how to implement AI concepts using Python. It covers core topics like search algorithms, machine learning, natural language processing, and neural networks. Learners are guided through building intelligent systems using popular Python libraries such as NumPy, Pandas, scikit-learn, and TensorFlow. The course includes hands-on examples like chatbots, recommendation systems, and predictive models. It balances theory and practical implementation, making it ideal for beginners and intermediate learners who want to understand AI development and apply it in real-world scenarios using Python .",
    "This beginner-friendly introduction to Data Science explains what data science is, its importance, and how it's used to extract insights from data. The tutorial covers the data science lifecycle, including data collection, cleaning, analysis, visualization, and modeling. It introduces key tools and technologies like Python, R, SQL, and libraries such as Pandas and Matplotlib. It also highlights roles like Data Scientist, Data Analyst, and ML Engineer, along with applications in business, healthcare, and more. Ideal for newcomers, the session offers a solid foundation in data-driven thinking and the skills needed to start a data science journey .",
    "This beginner-level tutorial explains the basics of Cloud Computing, its definition, features, and real-world applications. It covers the core service models—IaaS (Infrastructure as a Service), PaaS (Platform as a Service), and SaaS (Software as a Service)—along with deployment models like Public, Private, and Hybrid Cloud. The video discusses how cloud computing enables on-demand access to computing resources like servers, storage, and databases via the internet. It also introduces major providers like AWS, Azure, and Google Cloud, highlighting scalability, cost-efficiency, and flexibility. It’s perfect for beginners wanting to understand the fundamentals of cloud technology and its business impact.",
    "Generative AI is a type of artificial intelligence that creates new content like text, images, music, or code by learning patterns from data. It powers tools like ChatGPT and DALL·E. This tutorial explains its workings, applications, and ethical concerns, making it ideal for beginners exploring creative AI technologies.",
    "a directed graph is a graph where all the edges are directed . if you start from a node, you can go to four, but if I'm standing at four, I cannot come back to one . it's also a cyclic graph, which is common"
             ]
    #return render(request, 'course.html', {'course': course, 'course_iframe':a,'SUMMARY':SUMMARY})

    a={}
    for course_ in j.keys():
        course_iframe[course_] = course_list[c]
        a[course_]=SUMMARY[c]
        c += 1



    return render(request, 'course.html', {'course':course, 'course_iframe': course_iframe.get(course),'SUMMARY':a.get(course)})

def quiz(request):
    course = request.GET.get('course_')
    questions = j.get(course)
    count = int(request.GET.get('count', 0))

    question_id = int(request.GET.get('next_id', 1))
    if question_id == 20:
        feedback_cat ={ 19: 'Excellent',20: 'Excellent', 19: 'GOOD', 18: 'GOOD', 17: 'GOOD', 16: 'better', 15: 'better', 14: 'It is good to refer the course'}
        feedback_cat_score = feedback_cat.get(count,'Poor performance improve it')
        if feedback_cat_score is None:
            feedback_cat_score = 'Go back to Course'
            return render(request, 'result_feedback.html', {'course': course, 'flag': True, 'marks': count, 'feedback': feedback_cat_score, 'total_marks': question_id - 1})
        return render(request, 'result_feedback.html', {'course': course, 'marks': count, 'feedback': feedback_cat_score, 'total_marks': question_id - 1})
    if question_id != 1 and request.GET.get('act_ans') == request.GET.get('answer'):
        count += 1
    question = questions[question_id - 1]
    next_id = question_id + 1
    
    return render(request, 'quiz.html', {'course': course, 'question_id': question_id, 'next_id': next_id, 'question': question, 'count': count})