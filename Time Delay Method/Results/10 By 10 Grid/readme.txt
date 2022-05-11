This test was done on a SWE fluid with:
epsilon=1e-8
f0=1e-5
beta=1e-12
A=1e2
Forcing2=1e-5
dt=1e-1

3by3 Corner- the (1,1) to (3,3) corer was used for training and forecasting. (Tau is 20 not 17 for this one!!)

2by2 Off Center- the (5,7) to (6,8) square was recorded and forecasted.

5by5 near center- ranges from (2,2) to (7,7)

The Sparse Grid- Used 10 data points randomly selected:
81
22
15
55
92
63
38
10,5
56
85

To perform these 4 tests, Gaussian RBF's + MultiQudaric + Driving Wind was used.