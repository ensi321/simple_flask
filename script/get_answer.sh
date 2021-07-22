#!/bin/bash

# First param is url, second parm is question
ssh yfhe@gpugate1.cs.hku.hk -i /Users/yvetteho/.ssh/gpugate /userhome/34/yfhe/master_send_request.sh $1 $2
scp -i /Users/yvetteho/.ssh/gpugate yfhe@gpugate1.cs.hku.hk:/userhome/34/yfhe/result.txt /tmp/result.txt