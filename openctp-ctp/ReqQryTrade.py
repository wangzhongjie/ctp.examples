# @Project: https://github.com/Jedore/ctp.examples
# @File:    ReqQryTrade.py
# @Time:    05/06/2024 21:56
# @Author:  Jedore
# @Email:   jedorefight@gmail.com
# @Addr:    https://github.com/Jedore

from base_tdapi import CTdSpiBase, tdapi


class CTdSpi(CTdSpiBase):

    def req(self):
        """ 请求查询成交
        doc: https://ctpdoc.jedore.top/6.7.9/JYJK/CTHOSTFTDCTRADERSPI/REQQRYTRADE/
        """

        self.print("请求查询成交")
        req = tdapi.CThostFtdcQryTradeField()
        req.BrokerID = self._broker_id
        req.InvestorID = self._user_id
        # 以下条件均可单独作为过滤条件，一个都不填，查询全部成交
        # req.InstrumentID = "cu2507"
        # req.InstrumentID = "i2509"
        # req.ExchangeID = "SHFE"
        # req.TradeID = "         402"
        # req.TradeTimeStart = "17:00:49"
        # req.TradeTimeEnd = "17:00:42"
        self._check_req(req, self._api.ReqQryTrade(req, 0))

    def OnRspQryTrade(self, pTrade: tdapi.CThostFtdcTradeField, pRspInfo: tdapi.CThostFtdcRspInfoField,
                      nRequestID: int, bIsLast: bool):
        """ 请求查询成交响应 """

        self._check_rsp(pRspInfo, pTrade, is_last=bIsLast)

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
        
        # 提取关键信息
        parsed_record = {
            "trade_id": fields.get("TradeID", "").strip(),
            "instrument_id": fields.get("InstrumentID", "").strip(),
            "exchange_id": fields.get("ExchangeID", "").strip(),
            "direction": "买入" if fields.get("Direction", "0") == "1" else "卖出",
            "offset_flag": "开仓" if fields.get("OffsetFlag", "0") == "0" else "平仓",
            "volume": int(fields.get("Volume", "0")),
            "price": float(fields.get("Price", "0")),
            "trade_date": fields.get("TradeDate", "").strip(),
            "trade_time": fields.get("TradeTime", "").strip(),
            "trade_datetime": f"{fields.get('TradeDate', '')} {fields.get('TradeTime', '')}"
        }
        
        parsed_records.append(parsed_record)
    
    # 按交易时间排序
    parsed_records.sort(key=lambda x: datetime.strptime(x["trade_datetime"], "%Y%m%d %H:%M:%S"))
    
    # 统计总成交记录数
    total_records = len(parsed_records)
    
    # 计算总成交金额
    total_amount = sum(record["price"] * record["volume"] for record in parsed_records)
    
    # 按交易所分组统计
    exchange_stats = {}
    for record in parsed_records:
        exchange = record["exchange_id"]
        if exchange not in exchange_stats:
            exchange_stats[exchange] = {"count": 0, "volume": 0, "amount": 0}
        exchange_stats[exchange]["count"] += 1
        exchange_stats[exchange]["volume"] += record["volume"]
        exchange_stats[exchange]["amount"] += record["price"] * record["volume"]
    
    # 按合约分组统计
    instrument_stats = {}
    for record in parsed_records:
        instrument = record["instrument_id"]
        if instrument not in instrument_stats:
            instrument_stats[instrument] = {"count": 0, "volume": 0, "amount": 0}
        instrument_stats[instrument]["count"] += 1
        instrument_stats[instrument]["volume"] += record["volume"]
        instrument_stats[instrument]["amount"] += record["price"] * record["volume"]
    
    # 生成结果
    result = {
        "total_records": total_records,
        "total_amount": round(total_amount, 2),
        "exchange_stats": exchange_stats,
        "instrument_stats": instrument_stats,
        "records": parsed_records
    }
    
    return result

    
if __name__ == '__main__':
    spi = CTdSpi()
    spi.req()

    spi.wait_last()
