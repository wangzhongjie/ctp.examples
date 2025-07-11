# @Project: https://github.com/Jedore/ctp.examples
# @File:    ReqQryDepthMarketData.py
# @Time:    21/07/2024 14:42
# @Author:  Jedore
# @Email:   jedorefight@gmail.com
# @Addr:    https://github.com/Jedore

from base_tdapi import CTdSpiBase, tdapi


class CTdSpi(CTdSpiBase):

    def req(self):
        """ 请求查询行情，只能查询当前快照，不能查询历史行情。
        doc: https://ctpdoc.jedore.top/6.7.9/JYJK/CTHOSTFTDCTRADERSPI/REQQRYDEPTHMARKETDATA/
        """

        self.print("请求查询行情，只能查询当前快照，不能查询历史行情。")
        req = tdapi.CThostFtdcQryDepthMarketDataField()
        req.InstrumentID = 'AP410'  # 不传则查所有合约
        # 貌似仿真环境，不指定合约无法查询全部行情，只能单个查询返回
        self._check_req(req, self._api.ReqQryDepthMarketData(req, 0))

    def OnRspQryDepthMarketData(self, pDepthMarketData: tdapi.CThostFtdcDepthMarketDataField,
                                pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 请求查询行情响应 """

        self._check_rsp(pRspInfo, pDepthMarketData, is_last=bIsLast)


if __name__ == '__main__':
    spi = CTdSpi()
    spi.req()

    spi.wait_last()
