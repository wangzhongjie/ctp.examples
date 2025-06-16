import re
import json
from datetime import datetime

def parse_trade_records(log_content):
    # 提取交易记录部分
    trade_records_section = re.search(r'>>>>  请求查询成交.*?(?=\n\n|$)', log_content, re.DOTALL)
    if not trade_records_section:
        return {"error": "未找到交易记录"}
    
    trade_records_text = trade_records_section.group(0)
    
    # 提取每一条交易记录
    record_pattern = r'响应内容: ([^响应]+)'
    records = re.findall(record_pattern, trade_records_text)
    
    parsed_records = []
    for record in records:
        # 解析每条记录的键值对
        fields = {}
        for field in record.strip().split(','):
            if '=' in field:
                key, value = field.split('=', 1)
                fields[key.strip()] = value.strip()
        
        # 提取指定字段并映射到友好名称
        parsed_record = {
            "成交编号": fields.get("TradeID", "").strip(),
            "合约名称": fields.get("InstrumentID", "").strip(),
            "买卖方向": "买入" if fields.get("Direction", "0") == "0" else "卖出",
            "开平": "开仓" if fields.get("OffsetFlag", "0") == "0" else "平仓",
            "成交价格": float(fields.get("Price", "0")),
            "成交手数": int(fields.get("Volume", "0")),
            "手续费": 0,  # 原始记录中未提供
            "平仓盈亏": 0,  # 原始记录中未提供
            "平仓盈亏(逐笔)": 0,  # 原始记录中未提供
            "投保": "投机" if fields.get("HedgeFlag", "1") == "1" else "套期保值",
            "成交时间": f"{fields.get('TradeDate', '')} {fields.get('TradeTime', '')}",
            "成交类型": fields.get("TradeType", "").strip() or "普通成交",
            "交易所": fields.get("ExchangeID", "").strip()
        }
        
        parsed_records.append(parsed_record)
    
    # 按交易时间排序
    parsed_records.sort(key=lambda x: datetime.strptime(x["成交时间"], "%Y%m%d %H:%M:%S"))
    
    return parsed_records

# 读取日志文件或使用提供的内容
log_content = """
>>>>  请求查询成交
 [2025-06-13 09:55:28.588283]
 发送请求: BrokerID=2071,ExchangeID=,InstrumentID=,InvestUnitID=,InvestorID=35601428,TradeID=,TradeTimeEnd=,TradeTimeStart=
 响应内容: BrokerID=2071,BrokerOrderSeq=2052,BusinessUnit=           100000045,ClearingPartID=0030,ClientID=01565289,Direction=0,ExchangeID=DCE,ExchangeInstID=i2509,HedgeFlag=1,InstrumentID=i2509,InvestUnitID=,InvestorID=35601428,OffsetFlag=0,OrderLocalID=           3,OrderRef=           1,OrderSysID=   100000045,ParticipantID=0030,Price=675.0,PriceSource=0,SequenceNo=4,SettlementID=1,TradeDate=20250613,TradeID=   100000015,TradeSource=0,TradeTime=08:59:00,TradeType=0,TraderID=00302003,TradingDay=20250613,TradingRole= ,UserID=35601428,Volume=2
 响应内容: BrokerID=2071,BrokerOrderSeq=3339,BusinessUnit=           100008622,ClearingPartID=0030,ClientID=01565289,Direction=0,ExchangeID=DCE,ExchangeInstID=i2509,HedgeFlag=1,InstrumentID=i2509,InvestUnitID=,InvestorID=35601428,OffsetFlag=1,OrderLocalID=          78,OrderRef=           1,OrderSysID=   100008674,ParticipantID=0030,Price=764.5,PriceSource=0,SequenceNo=145,SettlementID=1,TradeDate=20250613,TradeID=   100000334,TradeSource=0,TradeTime=09:53:10,TradeType=0,TraderID=00302003,TradingDay=20250613,TradingRole= ,UserID=35601428,Volume=1
 响应内容: BrokerID=2071,BrokerOrderSeq=3151,BusinessUnit=           100005135,ClearingPartID=0030,ClientID=01565289,Direction=1,ExchangeID=DCE,ExchangeInstID=i2509,HedgeFlag=1,InstrumentID=i2509,InvestUnitID=,InvestorID=35601428,OffsetFlag=1,OrderLocalID=          58,OrderRef=           2,OrderSysID=   100005187,ParticipantID=0030,Price=762.5,PriceSource=0,SequenceNo=108,SettlementID=1,TradeDate=20250613,TradeID=   100000239,TradeSource=0,TradeTime=09:45:19,TradeType=0,TraderID=00302003,TradingDay=20250613,TradingRole= ,UserID=35601428,Volume=2
 响应内容: BrokerID=2071,BrokerOrderSeq=2053,BusinessUnit=           100000046,ClearingPartID=0030,ClientID=01565289,Direction=0,ExchangeID=DCE,ExchangeInstID=i2509,HedgeFlag=1,InstrumentID=i2509,InvestUnitID=,InvestorID=35601428,OffsetFlag=0,OrderLocalID=           4,OrderRef=           2,OrderSysID=   100000046,ParticipantID=0030,Price=675.0,PriceSource=0,SequenceNo=9,SettlementID=1,TradeDate=20250613,TradeID=   100000040,TradeSource=0,TradeTime=09:12:27,TradeType=0,TraderID=00302003,TradingDay=20250613,TradingRole= ,UserID=35601428,Volume=1
 响应内容: BrokerID=2071,BrokerOrderSeq=2053,BusinessUnit=           100000046,ClearingPartID=0030,ClientID=01565289,Direction=0,ExchangeID=DCE,ExchangeInstID=i2509,HedgeFlag=1,InstrumentID=i2509,InvestUnitID=,InvestorID=35601428,OffsetFlag=0,OrderLocalID=           4,OrderRef=           2,OrderSysID=   100000046,ParticipantID=0030,Price=675.0,PriceSource=0,SequenceNo=7,SettlementID=1,TradeDate=20250613,TradeID=   100000029,TradeSource=0,TradeTime=09:09:39,TradeType=0,TraderID=00302003,TradingDay=20250613,TradingRole= ,UserID=35601428,Volume=1
 响应内容: BrokerID=2071,BrokerOrderSeq=2045,BusinessUnit=           100000043,ClearingPartID=0030,ClientID=01565289,Direction=1,ExchangeID=DCE,ExchangeInstID=i2509,HedgeFlag=1,InstrumentID=i2509,InvestUnitID=,InvestorID=35601428,OffsetFlag=0,OrderLocalID=           2,OrderRef=           1,OrderSysID=   100000043,ParticipantID=0030,Price=675.0,PriceSource=0,SequenceNo=5,SettlementID=1,TradeDate=20250613,TradeID=   100000015,TradeSource=0,TradeTime=08:59:00,TradeType=0,TraderID=00302003,TradingDay=20250613,TradingRole= ,UserID=35601428,Volume=2
 """

# 解析交易记录
parsed_records = parse_trade_records(log_content)

# 打印交易记录总数
print(f"总成交记录数: {len(parsed_records)}")

# 保存JSON结果到文件
with open('trade_records.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_records, f, ensure_ascii=False, indent=2)

print(f"交易记录已保存到 trade_records.json")

# 打印前几条记录作为示例
print("\n前三条交易记录示例:")
for i, record in enumerate(parsed_records):
    print(f"\n记录 {i+1}:")
    for key, value in record.items():
        print(f"  {key}: {value}")
