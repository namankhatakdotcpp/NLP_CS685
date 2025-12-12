#!/bin/bash
# Monitor the training progress

echo "=== Training Status ==="
echo ""

# Check if process is running
PID=756789
if ps -p $PID > /dev/null 2>&1; then
    echo "✅ Training is RUNNING (PID: $PID)"
    echo ""
    
    # Show resource usage
    echo "Resource Usage:"
    ps aux | grep $PID | grep -v grep | awk '{printf "  CPU: %s%%  Memory: %s%%\n", $3, $4}'
    echo ""
else
    echo "❌ Training has STOPPED"
    echo ""
fi

# Show last 30 lines of log
echo "=== Recent Log (last 30 lines) ==="
tail -30 training_curved_mix.log

echo ""
echo "=== Commands ==="
echo "View full log:     tail -f training_curved_mix.log"
echo "Check process:     ps aux | grep 756789"
echo "Kill training:     kill 756789"
echo "Find checkpoints:  ls -lh outputs/parseq_finetune/*/checkpoints/"
