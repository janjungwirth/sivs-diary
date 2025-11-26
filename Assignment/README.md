# Lab Assignment: Securing a Web Application

**Disclaimer:**

> Please check off the tasks you have completed and for which you are prepared to give a presentation in class. The presentation can be in any visual or audiovisual form (e.g., PowerPoint, Flipchart, Demo, Code Example, or Program).
>
> **Important:** You must be able to convey the solution clearly.
>
>   * At least one task per teaching unit must be selected. Otherwise, participation in the practical part is considered unfulfilled.
>   * By checking a box, you agree to potentially be called upon to present your solution. If this happens and you are unable to present the solution, it will be counted as a failed attempt.
>   * More information can be found on Moodle under "Information on the 'Task Catalog' section".

-----

## Task Description

**Learner Lab Link:** [AWS Academy LMS Login](https://www.awsacademy.com/vforcesite/LMS_Login)

The goal is to properly secure a small web application. The script installs a small web app consisting of a website with JavaScript and a Flask API. Your task is to close potential security loopholes.

SQL Injections, XSS attacks, and unauthorized access to sensitive data are all possible. Find as many errors as possible. You may use any tools (BurpSuite, Postman, Google, AI Tools) to solve the tasks. The important part is developing an understanding of the subject matter.

### Installation Steps: AWS

1.  Create an **EC2 Instance** in the Learner Lab (Ubuntu, RAM: min. 1GB, HD: 30GB).
2.  Create a new IP address under the menu item **'Elastic IPs'** and assign it to your created server. This configures a static IP address for the server. The IP address remains preserved even after restarting the Learner Lab.
3.  Configure the **AWS Firewall** (Security Groups) so that all incoming connections are allowed.

### Installation Steps: Server

1.  Connect to the created server via SSH.
2.  Execute the following commands:

<!-- end list -->

```bash
mkdir -p /home/ubuntu/
rm -rf /home/ubuntu/sivs-diary
cd /home/ubuntu/
git clone https://github.com/fhtevssivs/sivs-diary.git
cd sivs-diary/sivs-diary/install/
sudo chmod +x ./install.sh 
sudo ./install.sh
```

You should now be able to access the web application via the AWS DNS Name (visible in the EC2 Console).

**Notes:**

  * `http://xxxx.freemyip.com:81/` =\> **PGADMIN**
  * `http://xxx.freemyip.com:80/` =\> **DIARY (Tagebuch)**

**Backend Control:**

```bash
sudo service sivs-diary_service (start|stop|restart)
```

**Credentials:**

  * **DB Client (PgAdmin):** Username: `admin@sivs.com`, Password: `sivs_2025!`
  * **DB User:** Username: `postgres`, Password: `sivs_2025!`

**Development Info:**
For this unit, it is necessary to make slight changes to Python code and JavaScript.

  * **IDE Recommendation:** [PyCharm](https://www.jetbrains.com/de-de/pycharm/)
  * **File Transfer:** You can exchange adapted files using WinSCP (Windows) or FileZilla (Linux). Alternatively, use editors like `nano` or `vi` directly on the server to fix security gaps.
  * **Apply Changes:** Run `sudo service sivs-diary_service restart` to load your changes.
  * *Alternative:* You can run the code for Tasks 6-10 directly from your IDE. Tasks 1-5 focus more on infrastructure.

-----

## Tasks

### 1\. Ports

**Identification of open ports**

  - [ ] **Task:**
      * **Question:** Which ports are open on your server?
      * **Instructions:** Use tools like `netstat`, `ss`, or `nmap` to identify the open ports on the server.
      * **Question 2:** How did you find the open ports, and what other possibilities exist to detect open ports?

### 2\. Firewall Configuration

**Firewall Configuration**

  - [ ] **Task:**
      * **Task:** Configure the server's firewall (`ufw`) so that only the necessary ports for HTTP, POSTGRES, and SSH are open.
      * **Instructions:** Research how to use `ufw` on an Ubuntu server to set up the firewall accordingly. Ensure that all other ports are blocked to prevent unnecessary access.

### 3\. Encrypted Connections

**Analysis of Encryption**

  - [ ] **Task:**
      * **Question:** Which connections on your server are encrypted?
      * **Instructions:** Use tools like `openssl`, `curl -v`, or `Wireshark` to check which connections on the server are encrypted.

### 4\. Implementation of TLS

**Create a Let's Encrypt Certificate**

  - [ ] **Task:**
      * **Task:** Generate a "Let's Encrypt" certificate using `certbot`.
      * **Questions:**
          * What is a "Let's Encrypt" certificate, and which organization is behind it?
          * What is essential for you to be able to request the certificate?
          * How long is such a certificate valid, and what happens after it expires?
      * **Instructions:** Also set up an automatic renewal system for the certificate, e.g., via a Cron Job, to ensure certificates are updated regularly.

### 5\. Analyze and Secure Apache Configuration

**Security Analysis of the Apache Service**

  - [ ] **Task:**
      * **Question:** Do you consider the Apache service to be sufficiently securely configured?
      * **Tasks:**
          * Investigate what users can view in the current Apache configuration.
          * Identify potential risks and vulnerabilities in the current configuration.
      * **Improvements:** List methods to increase the security of the Apache configuration, e.g., by disabling directory listings and limiting the information Apache reveals. Also, check if the user used for the service is appropriate.
      * *Hint:* Focus on the files `file-server.conf` and `envvars`.

### 6\. Code Analysis for SQL Injections

**Analyze and Fix SQL Injection**

  - [ ] **Task:**
      * **Task:** Analyze the code for possible SQL Injection vulnerabilities and fix them.
      * **Hint:** Use prepared statements and ORM techniques to mitigate SQL Injection risks.

### 7\. Code Analysis for XSS

**Analyze and Fix XSS Vulnerabilities**

  - [ ] **Task:**
      * **Task:** Check the code for possible Cross-Site Scripting (XSS) vulnerabilities and fix them.
      * **Hint:** Sanitize user inputs and use mechanisms to prevent malicious code (e.g., escaping HTML tags). Focus on `diary.html`.

### 8\. Code Analysis Authentication [Optional Presentation]

**Analysis and Improvement of Access Protection**

  - [ ] **Task:**
      * **Question:** Is access to resources and sensitive data sufficiently protected?
      * **Tasks:**
          * Ensure that users can only access data for which they have permissions.
          * Implement at least Basic Authentication to secure access.

### 9\. Content Security Policy (CSP) [Optional Presentation]

**Analysis**

  - [ ] **Task:**
      * **Question:** Analyze the provided Python code and check if a Content Security Policy (CSP) could reduce potential risks.
      * **Instructions:** Identify possible vulnerabilities in how content is included or executed and define policies that increase security.

### 10\. Cross-Origin Resource Sharing (CORS)

**Analysis**

  - [ ] **Task:**
      * **Question:** Analyze the Python code and formulate measures to ensure safe handling of Cross-Origin requests.
      * **Instructions:** Describe the risks and implement CORS headers and settings to prevent unauthorized use of resources.

-----

## Cheatsheets

### Firewall Configuration (`ufw`)

| Command | Example | Description |
| :--- | :--- | :--- |
| `ufw status` | `ufw status` | Shows firewall status and active rules. |
| `ufw show added` | `ufw show added` | Shows inactive rules as well. |
| `ufw enable` | `ufw enable` | Activates the firewall. |
| `ufw disable` | `ufw disable` | Deactivates the firewall. |
| `ufw default deny` | `ufw default deny` | Sets default policy for incoming traffic to Deny. |
| `ufw default allow` | `ufw default allow` | Sets default policy for incoming traffic to Allow. |
| `ufw allow [Port]` | `ufw allow 80/tcp` | Allows incoming traffic on the specified port/protocol. |
| `ufw deny [Port]` | `ufw deny 22/tcp` | Denies incoming traffic on the specified port/protocol. |
| `ufw limit [Port]` | `ufw limit 22/tcp` | Limits connection rate for specified port/protocol. |
| `ufw allow from [IP]` | `ufw allow from 192.168.1.1` | Allows incoming traffic from specified IP. |
| `ufw deny from [IP]` | `ufw deny from 10.0.0.1` | Denies incoming traffic from specified IP. |
| `ufw delete [Rule Number]`| `ufw delete 3` | Deletes the rule with the specified number. |
| `ufw reload` | `ufw reload` | Reloads firewall rules without dropping connections. |

### Let's Encrypt

The following commands allow generating a Let's Encrypt certificate via CertBot.

```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-apache

# Generate Cert for your domain
sudo certbot --apache -d yourdomain.com

# Restart Apache2
sudo systemctl restart apache2
```

### SQL Injection

**Insecure Code:**

```python
user_input = input("Enter your username: ")
query = "SELECT * FROM users WHERE username = '" + user_input + "';"
cursor.execute(query)
```

**Secure Code:**

```python
user_input = input("Enter your username: ")
query = "SELECT * FROM users WHERE username = %s;"
cursor.execute(query, (user_input,))
```

### XSS (Cross-Site Scripting)

  * **Reflected XSS:** The attacker introduces a malicious link that directs users to a manipulated page.
      * *Example:* `http://www.example.com/search?query=<script>alert('XSS')</script>`
  * **Persistent (Stored) XSS:** The attacker saves malicious code directly on the server, which is then retrieved by other users.
      * *Example:* An attacker inserts malicious code into a guestbook or comment field.
  * **DOM-based XSS:** The attack occurs on the user's side when the browser executes JavaScript code based on DOM manipulation.
      * *Example:* `http://www.example.com/#<script>alert('XSS')</script>`
  * **Image-based XSS:** The attacker hides malicious code in images or other resources (e.g., in metadata).

**Vulnerability Examples:**

| Method/Practice | Example | Susceptibility to XSS | Example of Malicious Input |
| :--- | :--- | :--- | :--- |
| **Insecure Input Validation** | `<input type="text" value="<?php echo $_GET['user']; ?>">` | Input not validated | `"><script>alert('XSS Exploit');</script>` |
| **Direct Insertion of User Input** | `<p>User Input: <?php echo $_GET['input']; ?></p>` | No checking or encoding | `"><script>alert('XSS Exploit');</script>` |
| **Insecure use of innerHTML** | `document.getElementById('elem').innerHTML = userData;` | Inserting unvalidated HTML | `<img src=x onerror="alert('XSS Exploit')">` |
| **Insecure JS Event Handling** | `<button onclick="<?php echo $_GET['action']; ?>">Click</button>` | Inserting unvalidated JS code | `"onmouseover="alert('XSS Exploit');"` |
| **Insecure URL Parameters** | `var data = "<?php echo $_GET['param']; ?>";` | Inserting unvalidated data | `"><script>alert('XSS Exploit');</script>` |
| **Use of eval()** | `eval(userProvidedCode);` | Execution of unvalidated code | `alert('XSS Exploit')` |

### Authentication Wrapper Methods

The method `requires_auth` checks if an Authorization Header is set (see MDN Web Docs). If this header exists and the user is authorized to access the resource, `getdiaryentries()` continues. Otherwise, a 401 Unauthorized status is returned.

**HTTP View:**

```python
@diary_blueprint.route('/api/diary', methods=['GET'])
@auth_handler.requires_auth
def getdiaryentries():
    username = request.args.get('username')
    result = db_handler.getDiary(username=username)
    return result
```

**Authentication Logic:**

```python
def check_auth(self, username, password):
    print(f"Checking {username} and {password}")
    user_query = "SELECT * FROM Users WHERE username = %s AND password = %s"
    result = self.db_handler.execute_query(user_query, (username, password), fetchone=True)
    return result is not None

def authenticate(self):
    return ('Authentication required', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(self, f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth:
            username = auth.username
            password = auth.password
        if not auth or not self.check_auth(username, password):
            return self.authenticate()
        
        requested_username = kwargs.get('username')
        if not requested_username:
            requested_username = request.args.get('username')
        if not requested_username:
            data = request.get_json()
            requested_username = data.get('username')
            
        if requested_username != auth.username:
            return self.authenticate()
            
        return f(*args, **kwargs)
    return decorated
```