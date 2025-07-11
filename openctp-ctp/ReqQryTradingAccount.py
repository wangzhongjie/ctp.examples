# @Project: https://github.com/Jedore/ctp.examples
# @File:    ReqQryTradingAccount.py
# @Time:    05/06/2024 21:59
# @Author:  Jedore
# @Email:   jedorefight@gmail.com
# @Addr:    https://github.com/Jedore

from base_tdapi import CTdSpiBase, tdapi


class CTdSpi(CTdSpiBase):

    def req(self):
        """ 请求查询资金账户
        doc: https://ctpdoc.jedore.top/6.7.9/JYJK/CTHOSTFTDCTRADERSPI/REQQRYTRADINGACCOUNT/
        """

        self.print("请求查询资金账户")
        req = tdapi.CThostFtdcQryTradingAccountField()
        req.BrokerID = self._broker_id
        req.InvestorID = self._user_id
        # req.CurrencyID = "CNY"
        self._check_req(req, self._api.ReqQryTradingAccount(req, 0))

    def OnRspQryTradingAccount(self, pTradingAccount: tdapi.CThostFtdcTradingAccountField,
                               pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 请求查询资金账户响应 """

        self._check_rsp(pRspInfo, pTradingAccount, is_last=bIsLast)


if __name__ == '__main__':
    spi = CTdSpi()
    spi.req()

    spi.wait_last()
