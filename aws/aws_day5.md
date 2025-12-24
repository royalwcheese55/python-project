1. What is an EC2 instance in simple terms?
An EC2 instance is basically a virtual computer in the cloud provided by Amazon Web Services (AWS).
like renting a computer over the internet and you can choose how powerful it is like cpu and memory, typically use to run a website or api.

2. What is the difference between vertical scaling and horizontal scaling?
vertical: increase the power of single machine. e.g add more cpu/ram
it is single to implement but has a hard limit/ single point of faliure

horizontal: add more machine and distribute the load, like add more containers or instances
better scalability, no single point failure, high availability but more complex.

3. Why do big data systems prefer horizontal scaling?
it is the only practical way to handle massive data and traffic reliably and cheaply. Data volume will exceeds single-machine limits if we use vertical. and fault tolerance is required in big data. it is cheaper do scale horizontal and big data process data in parallel.

4. If you terminate an EC2 instance, why might AWS still charge you?
because related resources like EBS volumes, snapshots, or Elastic IPs continue to exist and are billed separately.
    
