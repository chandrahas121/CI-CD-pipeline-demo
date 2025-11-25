pipeline {
    agent any

    environment {
        // 1) Change IMAGE to your Docker Hub repo (roll-number based)
        // Example if your roll is IMT2023XXX and DockerHub user is harsh9163:
        // IMAGE = "harsh9163/imt2023xxx-todo-cli:jenkins"
        IMAGE = "chandrahas121/imt2023037:jenkins"
        VENV = ".venv"
    }

    stages {

        stage('Checkout') {
            steps {
                // 2) Point this to YOUR GitHub repo (the To-Do project)
                checkout([$class: 'GitSCM',
                  branches: [[name: '*/main']],  // or '*/master' if your branch is master
                  userRemoteConfigs: [[
                    url: 'https://github.com/chandrahas121/CI-CD-pipeline-demo.git',
                    credentialsId: 'github-creds'
                  ]]
                ])
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat 'python -m venv %VENV%'
                bat '%VENV%\\Scripts\\python.exe -m pip install --upgrade pip'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '%VENV%\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat '%VENV%\\Scripts\\pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE% .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                  usernameVariable: 'USER',
                                                  passwordVariable: 'PASS')]) {
                    bat """
                    echo %PASS% | docker login -u %USER% --password-stdin
                    docker push %IMAGE%
                    """
                }
            }
        }

        // Optional for CLI app; keep if teacher wants container run
        stage('Deploy Container') {
            steps {
                bat """
                docker pull %IMAGE%
                docker stop todo-cli || exit 0
                docker rm todo-cli || exit 0
                docker run -d --name todo-cli %IMAGE%
                """
            }
        }
    }
}