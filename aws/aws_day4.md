1. Why is Amazon S3 considered Object Storage instead of a file system?
S3 stores data as objects inside a flat key-value namespace, not as files inside hierarchical folders with a real directory structure, S3 only have key prefixes, and does not support posix file system operations
S3 is object storage because it stores data as immutable objects in a flat key-value namespace with no real directories or filesystem semantics like locking, appends, or atomic operations.

2. Explain the relationship between Bucket, Object, and Key in S3.
bucket- top level container that hold all the data
object- actual stored data, contains: key, data, metadata(immutable)
key- is a unique identifier for object within a bucket

3. Why can’t you update a single row inside a CSV file stored in S3?
Because S3 is object storage, not a file system — objects are immutable, so you cannot modify part of a file.
To “update one row,” you must rewrite the entire CSV file as a new object.

4. What is an S3 prefix, and why is it important for Spark / Hive performance?
An S3 prefix is the path-like beginning of an object key that acts like a virtual folder.
it is critical for Spark/Hive performance because it enables parallel file listing, faster scans, and efficient partition pruning.

5. Compare IAM Policy, Bucket Policy, and Access Point Policy.
IAM- who the user/role is allowed to access, control permissions
BUcket- control access to the bucket only, grant access to other aws acount
access point- control access to specific access point to bucket, enforce network restrictions(VPC-only access)

6. What problem does S3 Versioning solve, and what new problem does it introduce?
S3 Versioning protects against accidental deletion or overwriting of objects. It increases storage cost because S3 keeps every version of every object.

7. What is the difference between SRR and CRR in S3 replication?
Same-Region Replication: Replicates objects from one S3 bucket to another bucket in the same AWS region. used for backup within same region and staging.
Cross-Region Replication: Replicates objects to a bucket in a different AWS region. used for disaster recovery and lower latency.
