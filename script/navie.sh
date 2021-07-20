#!/bin/bash

scp -i /Users/yvetteho/.ssh/gpugate $1 yfhe@gpugate1.cs.hku.hk:/tmp/request.txt
ssh yfhe@gpugate1.cs.hku.hk -i /Users/yvetteho/.ssh/gpugate /userhome/34/yfhe/master_send_request.sh /tmp/request.txt
scp -i /Users/yvetteho/.ssh/gpugate yfhe@gpugate1.cs.hku.hk:/userhome/34/yfhe/result.txt /tmp/result.txt