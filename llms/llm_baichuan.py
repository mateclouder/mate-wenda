from plugins.common import settings

def chat_init(history):
    history_formatted = None
    if history is not None:
        history_formatted = []
        tmp = []
        for i, old_chat in enumerate(history):
            if len(tmp) == 0 and old_chat['role'] == "user":
                tmp.append(old_chat['content'])
            elif old_chat['role'] == "AI" or old_chat['role'] == 'assistant':
                tmp.append(old_chat['content'])
                history_formatted.append(tuple(tmp))
                tmp = []
            else:
                continue
    return history_formatted


def chat_one(prompt, history_formatted, max_length, top_p, temperature, zhishiku=False):
    yield str(len(prompt))+'字正在计算'
    if max_length>100:
        max_length=100
    inputs = tokenizer(prompt, return_tensors='pt')
    inputs = inputs.to('cuda:0')
    pred = model.generate(**inputs, max_new_tokens=max_length, do_sample=True)
    yield tokenizer.decode(pred.cpu()[0], skip_special_tokens=True)

# def sum_values(dict):
#     total = 0
#     for value in dict.values():
#         total += value
#     return total

# def dict_to_list(d):
#     l = []
#     for k, v in d.items():
#         l.extend([k] * v)
#     return l

def load_model():
    global model, tokenizer
    strategy = ('->'.join([x.strip() for x in settings.llm.strategy.split('->')])).replace('->', ' -> ')
    s = [x.strip().split(' ') for x in strategy.split('->')]
    print(s)
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(settings.llm.path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(settings.llm.path, trust_remote_code=True)
    model = model.half()
    model = model.cuda()
    model = model.eval()
    # device, precision = s[0][0], s[0][1]
    # # 根据设备执行不同的操作
    # if device == 'cpu':
    #     # 如果是cpu，不做任何操作
    #     pass
    # elif device == 'cuda':
    #     # 如果是gpu，把模型移动到显卡
    #     import torch
    #     if not (precision.startswith('fp16i') and torch.cuda.get_device_properties(0).total_memory < 1.4e+10):
    #         model = model.cuda()
    # elif len(s)>1 and device.startswith('cuda:'):
    #     pass
    # else:
    #     # 如果是其他设备，报错并退出程序
    #     print('Error: 不受支持的设备')
    #     exit()
    # # 根据精度执行不同的操作
    # if precision == 'fp16':
    #     # 如果是fp16，把模型转化为半精度
    #     model = model.half()
    # elif precision == 'fp32':
    #     # 如果是fp32，把模型转化为全精度
    #     model = model.float()
    # elif precision.startswith('fp16i'):
    #     # 如果是fp16i开头，把模型转化为指定的精度
    #     # 从字符串中提取精度的数字部分
    #     bits = int(precision[5:])
    #     # 调用quantize方法，传入精度参数
    #     model = model.quantize(bits)
    #     if device == 'cuda':
    #         model = model.cuda()
    #     model = model.half()
    # elif precision.startswith('fp32i'):
    #     # 如果是fp32i开头，把模型转化为指定的精度
    #     # 从字符串中提取精度的数字部分
    #     bits = int(precision[5:])
    #     # 调用quantize方法，传入精度参数
    #     model = model.quantize(bits)
    #     if device == 'cuda':
    #         model = model.cuda()
    #     model = model.float()
    # else:
    #     # 如果是其他精度，报错并退出程序
    #     print('Error: 不受支持的精度')
    #     exit()
    # if len(s)>1:
    #     model = dispatch_model(model, device_map=device_map)
    # model = model.eval()
