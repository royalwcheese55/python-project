1. What is the difference between a transformation and an action in Spark? Give at least 3 examples of each.
Transformations are lazy operations that build the DAG, while actions force Spark to execute the DAG and return results or write output.
transformations: map() join() groupby()
action: count() collect() show()

2. Why does spark.read.csv() load all columns as StringType by default? What problems can this cause in aggregation or filtering?
because csv file have no schemam, so it treat every column as a string, unless you enable inferschema = True.
it can cause aggregation can't work correctly, or filter incorrectely, basically anything involve with numerical or date operations perform incorrect.


3. What does explode() do in Spark? In what scenario can explode() cause serious performance issues?
explode() takes an array or map column and converts each element into a new row, multiplying the number of rows.
it can cause severe performance issues when arrays are large or when row explosion leads to huge shuffles and memory pressure.

4. Why is groupBy() considered a wide transformation? What happens under the hood when a wide transformation is executed?
groupBy() is a wide transformation because Spark must bring together all rows with the same key, and those rows may exist in multiple different partitions across the cluster.
it performs a shuffle, that partition/ data move across network/ write intermediate files/ new stage boundary/ sorting and combining.

