from bhv.np import NumPyBoolBHV as BHV

Mary, home = BHV.nrand(2)
walked, ran, drove = BHV.nrand(3)

datapoints = [
    Mary ^ walked ^ home,
    Mary ^ ran ^ home,
    Mary ^ drove ^ home,
]

expected = Mary ^ BHV.majority3(walked, ran, drove) ^ home

assert BHV.majority(datapoints) == expected
