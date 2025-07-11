# @Project: https://github.com/Jedore/ctp.examples
# @File:    ReqQryInstrument.py
# @Time:    22/07/2024 14:01
# @Author:  Jedore
# @Email:   jedorefight@gmail.com
# @Addr:    https://github.com/Jedore

from base_tdapi import CTdSpiBase, tdapi


class CTdSpi(CTdSpiBase):

    def req(self):
        """ 请求查询合约
        doc: https://ctpdoc.jedore.top/6.7.9/JYJK/CTHOSTFTDCTRADERSPI/REQQRYINSTRUMENT/
        """

        self.print("请求查询合约")
        req = tdapi.CThostFtdcQryInstrumentField()
        self._check_req(req, self._api.ReqQryInstrument(req, 0))

    def OnRspQryInstrument(self, pInstrument: tdapi.CThostFtdcInstrumentField, pRspInfo: tdapi.CThostFtdcRspInfoField,
                           nRequestID: int, bIsLast: bool):
        """ 请求查询合约响应 """

        self._check_rsp(pRspInfo, pInstrument, is_last=bIsLast)


if __name__ == '__main__':
    spi = CTdSpi()
    spi.req()

    spi.wait_last()
