*** Variables ***
&{Partition_US}   partitionName=AutoTest_Acc_{rand_str}  clusterName=${bossCluster}   add_sites=False
&{Partition_AUS}   partitionName=AutoTest_Acc_{rand_str}  clusterName=${bossCluster}   add_sites=True    localAreaCode=2
&{Partition_UK}   partitionName=AutoTest_Acc_{rand_str}  clusterName=${bossCluster}   add_sites=True    localAreaCode=28