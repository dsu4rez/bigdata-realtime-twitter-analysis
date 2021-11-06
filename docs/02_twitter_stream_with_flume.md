# Real-Time Twitter Analysis 2: Twitter Stream with Flume

We already discussed the architecture for this project in my previous post here. Now, it’s time for jumping into the mood and start working on it. The first step is to ingest the Twitter Stream into our cluster. For this task, we’ll use Apache Flume and Apache Kafka, which in conjunction are also known as Flafka.

Before starting with the implementation, let’s explain what Apache Flume is, and for what is used.

## What is Apache Flume?
Flume is a high-performance system that is widely used for data collection of any streaming event data. It supports aggregating data from many sources into HDFS, and it’s horizontally-scalable, extensible, and reliable.

The achitecture of Flume consists of four main components:

- Source: Receives events from an external source that generates them.
- Channel: It acts like a buffer that keeps the events from the source until they are drained by the sink.
- Sink: Sends an event to a specific destination.
- Agent: It’s a Java process that configures and hosts the source, channel, and sink.

The agents are configured with a Java Property file where we can define all the components we like to use for our use case.

Flume by default incorporates some built-in data sources ready to use for Syslog, Netcat, Exec, Spooldir, HTTP, or Kafka. And also, some sinks for Logger, IRC, HDFS, Kafka, or HBase. The channels available by default are memory (extremely fast but not reliable), file (slower but reliable), and Kafka (scalable and highly available). Besides these built-in implementations, we can also create our own if we like.

Flume also supports other ways to customize data flow that can inspect, modify or transform event data on-the-fly by implementing interceptors, or control the format of messages when they are written to the destination with event serializers.

Here you can see a map that illustrates the whole Flume architecture.

