import subprocess
import os

def execute_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(e)

def install_java():
    execute_command("sudo apt update")
    execute_command("sudo apt install openjdk-8-jdk")

def setup_ssh():
    execute_command("sudo apt install ssh")
    execute_command("ssh-keygen -t rsa -P \"\" -f ~/.ssh/id_rsa")
    execute_command("cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys")

def extract_hadoop():
    execute_command("sudo tar -xzvf ~/Downloads/hadoop-2.10.2.tar.gz -C /usr/local")

def configure_hadoop():
    # Update JAVA_HOME in hadoop-env.sh
    hadoop_env_path = "/usr/local/hadoop-2.10.2/etc/hadoop/hadoop-env.sh"
    java_home = "/usr/lib/jvm/java-8-openjdk-amd64"  # Adjust this path as per your system configuration
    with open(hadoop_env_path, "a") as f:
        f.write(f"\nexport JAVA_HOME=/usr\n")

    # Update core-site.xml
    with open("/usr/local/hadoop-2.10.2/etc/hadoop/core-site.xml", "w") as f:
        f.write("""<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>""")

    # Update hdfs-site.xml
    with open("/usr/local/hadoop-2.10.2/etc/hadoop/hdfs-site.xml", "w") as f:
        f.write("""<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value> <!-- Set your desired replication factor -->
    </property>
    <!-- Add other configurations as needed -->
</configuration>""")

    # Update mapred-site.xml
    with open("/usr/local/hadoop-2.10.2/etc/hadoop/mapred-site.xml", "w") as f:
        f.write("""<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <!-- Add other configurations as needed -->
</configuration>""")

    # Update yarn-site.xml
    with open("/usr/local/hadoop-2.10.2/etc/hadoop/yarn-site.xml", "w") as f:
        f.write("""<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <!-- Add other configurations as needed -->
</configuration>""")

def start_hadoop():
    execute_command("/usr/local/hadoop-2.10.2/bin/hdfs namenode -format")
    execute_command("/usr/local/hadoop-2.10.2/sbin/start-dfs.sh")
    execute_command("/usr/local/hadoop-2.10.2/sbin/start-yarn.sh")

def modify_bashrc():
    bashrc_path = os.path.expanduser("~/.bashrc")
    with open(bashrc_path, "a") as f:
        f.write("\n# Hadoop Path\n")
        f.write("export HADOOP_HOME=/usr/local/hadoop-2.10.2\n")
        f.write("export PATH=$PATH:$HADOOP_HOME/bin\n")
        f.write("export PATH=$PATH:$HADOOP_HOME/sbin\n")
def main():
    install_java()
    setup_ssh()
    extract_hadoop()
    configure_hadoop()
    start_hadoop()
    modify_bashrc()
    
    execute_command("source ~/.bashrc")

    # Enlist all nodes
    execute_command("jps")

if __name__ == "__main__":
    main()
