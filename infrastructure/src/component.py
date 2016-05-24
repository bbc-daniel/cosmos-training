from BBC.AWS.CloudFormation.Common.Component import Component

component = Component("component-name")
component.set_health_check_url("/status")
component.render()