from BBC.AWS.CloudFormation.Common.Component import Component
from BBC.AWS.CloudFormation import AutoScaling

component = Component("rchatley-cosmos-training-2")
component.set_health_check_url("/status")

##  This references the default AutoScaling Group Name
asg_dimensions = [("AutoScalingGroupName", { "Ref": "ComponentAutoScalingGroup" })]

## This defines how many instances we want to scale up by when an alarm is triggered
scaleUpScalingPolicy=AutoScaling.ScalingPolicy("UpComponent","ChangeInCapacity",{"Ref": "ComponentAutoScalingGroup"},"1")
scale_up_actions=   [scaleUpScalingPolicy]

## This defines how many instances we want to scale down by when an alarm is triggered
scaleDownScalingPolicy=AutoScaling.ScalingPolicy("DownComponent","ChangeInCapacity",{"Ref": "ComponentAutoScalingGroup"},"-1")
scale_down_actions=   [scaleDownScalingPolicy]

## This defines the min/max number of instances allowed so we wont scale up or down past these values
component.set_autoscaling_range(1,3)

#This sets up the scale up alarm
# This says if the average CPU use over 60 seconds is greater than 80% for 3 consecutive periods then apply the scale up action to the auto scaling group
component.add_alarm("CPUUtilizationScaleUp",scale_up_actions,asg_dimensions, "GreaterThanOrEqualToThreshold", 2, "CPUUtilization", "AWS/EC2", 60, "Average", 80)

#This sets up the scale down  alarm
# This says if the average CPU use over 120 seconds is less than 20% for 3 consecutive periods then apply the scale down action to the auto scaling group
component.add_alarm("CPUUtilizationScaleDown",scale_down_actions,asg_dimensions, "LessThanThreshold", 3, "CPUUtilization", "AWS/EC2", 120, "Average", 20)

component.template.attach(scaleUpScalingPolicy)
component.template.attach(scaleDownScalingPolicy)

component.render()