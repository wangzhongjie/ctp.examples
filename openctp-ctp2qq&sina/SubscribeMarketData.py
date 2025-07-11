# @Project: https://github.com/Jedore/ctp.examples
# @File:    SubscribeMarketData.py
# @Time:    09/10/2024 13:00
# @Author:  Jedore
# @Email:   jedorefight@gmail.com
# @Addr:    https://github.com/Jedore

from base_mdapi import CMdSpiBase, mdapi


class CMdSpi(CMdSpiBase):

    def req(self, instruments):
        """ 订阅行情
        doc: https://ctpdoc.jedore.top/6.7.9/HQJK/CTHOSTFTDCMDAPI/SUBSCRIBEMARKETDATA/
        """

        self.print("订阅行情")
        encode_instruments = [i.encode('utf-8') for i in instruments]
        self._check_req(instruments, self._api.SubscribeMarketData(encode_instruments, len(instruments)))

    def OnRspSubMarketData(self, pSpecificInstrument: mdapi.CThostFtdcSpecificInstrumentField,
                           pRspInfo: mdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 订阅行情响应 """

        self._check_rsp(pRspInfo, pSpecificInstrument, is_last=bIsLast)

    def OnRtnDepthMarketData(self, pDepthMarketData: mdapi.CThostFtdcDepthMarketDataField):
        """ 行情通知 """
        self._print_rtn(pDepthMarketData, '行情通知')


if __name__ == '__main__':
    spi = CMdSpi()
    spi.req(["600000", "000001", "00700", "AAPL"])

    spi.wait_last()
