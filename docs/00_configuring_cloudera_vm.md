# Installing Spark 2 and Kafka on Cloudera’s Quickstart VM

As you probably know, to operate with Big Data, we need a cluster of several nodes. Unfortunately, people normally don’t have access to any of them. If we want to learn how to use the technologies behind, we need to make use of VMs with a pseudo cluster assembled in it, and a set of tools pre-installed and ready to use. Like is the case of the Cloudera’s Quickstart VM, that incorporates the Cloudera distribution of Hadoop (CDH), and a set of tools like Spark, HDFS, Hive, and Flume, among others.

During this post, I am going to show you how to set up and configure the latest Cloudera’s Quickstart VM (CDH 5.13), to get it ready to use with the latest version of Spark (2.4) and Kafka. The environment set here, it is going to be used in my personal Big Data projects you’ll be able to find in this blog.

## Downloading the VM

First of all, we need to download the Cloudera’s Quickstart VM (CDH 5.13) from here.

In this case, I opted for the VMWare option. After the file is downloaded, uncompress the rar-file, and mount the VM. Before launching it, I recommend doing some configuration tunning like increasing the RAM size (Cloudera Manager requires at least 8GB) and processor cores used.

Once launched, we will see a CentOS running with the CDH Hadoop distribution of Cloudera and the most common toolset for this kind of environments. We can list the software versions installed by opening a terminal and running:

```rpm -qa```

In this case, we find the following tools installed:

- Spark 1.6
- Flume 1.6
- Hive 1.1
- Impala 2.10
- Oozie 4.1.0

We notice that Kafka is not included in this package, and after taking a look at the websites of the installed tools, we see that all of them are a bit outdated. Cloudera provides a repository with the tools that are compatible with this particular CDH, so I recommend to install and update the tools you need using this repository.

In this particular case, I am interested in updating Spark to the latest version (2.4), because event if Spark 1.6 is very robust and provide good performance, Spark 2 was released in 2016 including exceptional improvements in features and performance. Moreover, I will install Kafka, because I plan to use it in one of my personal projects.

In order to save time and avoid possible complications, let’s use Cloudera Manager. CM is a web application provided by Cloudera that allows us to manage our cluster, the services and tools running, install/update tools, and see some performance metrics.

## Installing Cloudera Manager

By default, Cloudera Manger is not installed in our VM, so we need to install it. For that, we just need to go to Desktop and execute the “Launch Cloudera Express” script. After a while, we’ll get CM installed and running. We can check it by opening a browser and accessing to http://quickstart.cloudera:7180. We can log in using “cloudera” as user and password.

To make even easier the installation of software into our cluster, we are going to use “Parcels”. However, we have to configure it first by going to Desktop and running the “Migrate to Parcels” script. Once the script has fisnished we need to restart all the services on the cluster. We can do this by going to the Cloudera Manager Web UI, and clicking on the button next to the Cluster Name, and clicking Start.

## Installing Spark 2

Now that Cloudera Manager is already installed and configured to use Parcels, we can proceed to update our cluster to use Spark 2.

Unfortunately, the Java JDK version installed in this machine is 1.6 and Spark 2 requires Java JDK 1.8 version, therefore we need to update Java first.

### Pre-installation: updating Java JDK to version 1.8

Before proceeding, we will stop the cluster and all the services running in order to avoid possible problems. We can do it by going to Cloudera Manager UI, stopping the Cloudera Management Services, and the cluster. Then, open a terminal and stop the CM agent and server services:

```
sudo su
service cloudera-scm-agent stop
service cloudera-scm-server stop
```

Now, let’s proceed to install Java JDK 1.8. Open a terminal and run:

```sudo yum install java-1.8.0-openjdk```

Set JAVA_HOME environment variable in every place needed (~/.bash_profile (run scirpt after it), /etc/default/cloudera-scm-server, and /etc/default/bigtop-utils).

```export JAVA_HOME=/usr/lib/jvm/jre-1.8.0-openjdk.x86_64```

And also add the following lines to /etc/bashrc and run the script.

```
export JAVA_HOME=/usr/lib/jvm/jre-1.8.0-openjdk.x86_64
export JRE_HOME=${JAVA_HOME}
export JDK_HOME=${JAVA_HOME}
export ANT_HOME=/usr/local/apache-ant/apache-ant-1.9.2
export M2_HOME=/usr/local/apache-maven/apache-maven-3.0.4
export PATH=/usr/local/firefox:/sbin:$JAVA_HOME/bin:$ANT_HOME/bin:$M2_HOME/bin:$PATH
```

Check that Java version has been updated:

```java -version```

Now, open a terminal and start the CM agent and server services again.

```
sudo su
service cloudera-scm-agent start
service cloudera-scm-server start
```
Now we need to ask our cluster to use the Java JDK 1.8 to run all the services. Open a browser, navigate to Cloudera Manager UI, and go to Hosts, Configuration -> Advanced. There, look for the “Java Path” parameter, and type in the Java path (“/usr/lib/jvm/jre-1.8.0-openjdk.x86_64″).

We can proceed now to restart the Cloudera Management Services, and the cluster. Wait till all the services are up and running and check if all the Hadoop processes are using the new Java version. Open a terminal and type:

```ps -eaf | grep hadoop```

### Now yes… Installing Spark 2

Select the version of Spark 2 you want to install from here (in this case 2.4.0) and copy the CSD URL (http://archive.cloudera.com/spark2/csd/SPARK2_ON_YARN-2.4.0.cloudera1.jar).

Open a Terminal, download the CSD, set permissions and ownership to “cloudera–scm, and restart the “cloudera-scm-server”:

```
sudo su
cd /opt/cloudera/csd
wget http://archive.cloudera.com/spark2/csd/SPARK2_ON_YARN-2.4.0.cloudera1.jar
chown cloudera-scm:cloudera-scm SPARK2_ON_YARN-2.4.0.cloudera1.jar
chmod 644 SPARK2_ON_YARN-2.4.0.cloudera1.jar
service cloudera-scm-server restart
```

After that, open the Cloudera Manager UI, and restart the Cloudera Management Services and the Cluster Services.

Now, let’s install the Spark 2 parcel. In Cloudera Manager, navigate to Hosts –> Parcels, locate the Spark 2 parcel from the list, click on Download, then Distribute, and finally Activate.

Move back to the home page of CM, click on the button close to the Cluster Name, and select “Add service”. Select Spark 2; select the dependencies you need (in this case HDFS, Hive, and HBase); select the only instance available as History Server and Gateway, and leave the rest of configurations by default. After a while, Spark 2 will be up and running.

Spark 2 is now installed, you can test it by running some jobs in spark2-shell or pyspark2, but… wait… PySpark2 is not working!! Exactly, that is because PySpark2 requires Python 2.7, and this VM has Python 2.6 instead, so… Let’s install it too.

### Fixing PySpark2: updating to Python 2.7

Install GCC to compile Python Source:

```yum install gcc openssl-devel bzip2-devel```

Download Python 2.7 and uncompress it:

```
cd /usr/src
wget https://www.python.org/ftp/python/2.7.16/Python-2.7.16.tgz
tar xzf Python-2.7.16.tgz
```

Install Python 2.7:
```
cd Python-2.7.16
./configure --enable-optimizations
make altinstall
```

Check that Python 2.7 is installed:

```/usr/local/bin/python2.7 -V```

Set environment variable to make PySpark use Python 2.7 by editing and running ~/.bash_profile:

```export PYSPARK_PYTHON=/usr/local/bin/python2.7```

After this, we are able to use PySpark2 with no problems, and Spark 2 is ready to use.

## Installing Kafka

We are going to proceed to install Kafka in our “cluster”. Fortunately, this time the installation process is so much easier.

First, we need to install the Kafka parcel. Select the version of Kafka you want to install from here (in this case 3.1.1) and copy the Parcel URL (http://archive.cloudera.com/kafka/parcels/3.1.1/). In Cloudera Manager, navigate to Hosts –> Parcels, now click Configuration, and add the PARCEL_URL to the list under Remote Parcel Repository URLs, and click Save.

Locate the Kafka parcel from the list, click on Download, then Distribute, and finally Activate.

Move back to the home page of CM, click on the button close to the Cluster Name, and select “Add service”. Select Kafka; select the only instance available as Kafka Broker and Gateway, and leave the rest of configurations by default.

After a while, you will see that Kafka tries to start but the Broker goes down at first. This is due to some incorrect default configurations that cannot be set until after the Kafka Service has been added.

Go to the Home Page of CM, click on Kafka –> Configuration, and set the following parameters, and Save the changes:

```
Java Heap Size of Broker (broker_max_heap_size) =“256”
Advertised Host (advertised.host.name) = “quickstart.cloudera”
Inter Broker Protocol = “PLAINTEXT”
```

Restart the Kafka service from the CM home page, and after that, we will have Kafka up and running.

We can test it by opening a Terminal and creating Kafka topic, and listing the topics:
```
kafka-topics --zookeeper quickstart.cloudera:2181 --create --topic test --partitions 1 --replication-factor 1
kafka-topics --zookeeper quickstart.cloudera:2181 --list
```
Finally, we have set up our Cloudera’s Quickstart VM and is ready to start developing our personal projects with Spark 2 and Kafka.
