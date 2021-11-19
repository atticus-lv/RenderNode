# if self.operate_type == 'TEXT_2_STR':
#     self.remove_input('value1')
#     self.create_input('RenderNodeSocketText', 'text', 'Text')
# else:
#     self.remove_input('text')
#     self.create_input('RenderNodeSocketString', 'value1', 'Value')
#
# if self.operate_type == 'INT_2_STR':
#     self.remove_input('value1')
#     self.create_input('RenderNodeSocketInt', 'int', 'Int')
# else:
#     self.remove_input('int')
#     self.create_input('RenderNodeSocketString', 'value1', 'Value')
#
# if self.operate_type == 'STR_2_INT':
#     self.remove_output('output')
#     self.create_output('RenderNodeSocketInt', 'int', 'Int')
# else:
#     self.remove_output('int')
#     self.create_output('RenderNodeSocketString', 'output', 'Output')
#
# ('', 'Conversion', ''),
# ('INT_2_STR', 'Int to String', ''),
# ('STR_2_INT', 'String to Int', ''),
# ('TEXT_2_STR', 'Text to String', ''),