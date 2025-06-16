# @Project: https://github.com/Jedore/ctp.examples
# @File:    ReqOrderInsert.py
# @Time:    06/06/2024 22:21
# @Author:  Jedore
# @Email:   jedorefight@gmail.com
# @Addr:    https://github.com/Jedore
# .\venv_py312\Scripts\activate

from base_tdapi import CTdSpiBase, tdapi


class CTdSpi(CTdSpiBase):

    def req(self):
        """ 报单录入请求
        doc: https://ctpdoc.jedore.top/6.7.9/JYJK/CTHOSTFTDCTRADERSPI/REQORDERINSERT/
        """

        self.print("报单录入请求")

        # 注意选择一个相对活跃的合约及合适的价格
        # self.order_insert('SHFE', 'au2510', 780.32)
        # self.order_insert('SHFE', 'rb2510', 2976)
        # self.order_insert('SHFE', 'cu2507', 79220)
        # self.market_order_insert('SHFE', 'cu2507')
        # self.market_order_insert('DCE', 'i2509', 2)
        # self.order_insert('SHFE', 'cu2507', 79250, 2, 0, 0, 0) # 买开
        # self.order_insert('SHFE', 'cu2507', 79250, 2, 0, 1, 0) # 卖开
        # self.order_insert('SHFE', 'cu2507', 79250, 2, 0, 0, 1)  # 买平
        # self.order_insert('SHFE', 'cu2507', 79250, 2, 0, 1, 1)  # 卖平

        self.order_insert('SHFE', 'rb2510', 5100, 2, 0, 0, 0) # 买开

        # self.order_insert('DCE', 'i2509', 675, 2, 0, 0, 0) # 买开
        # self.order_insert('DCE', 'i2509', 675, 2, 0, 1, 0) # 卖开
        # self.order_insert('DCE', 'i2509', 764.5, 1, 0, 0, 1)  # 买平
        # self.order_insert('DCE', 'i2509', 710, 2, 0, 1, 1)  # 卖平

        # self.order_insert('CFFEX', 'IF2506', 3870, 1, 0, 0, 0) # 买开
        # self.order_insert('CFFEX', 'IF2506', 3890, 1, 0, 1, 0) # 卖开
        # self.order_insert('CFFEX', 'IF2506', 3882, 2, 0, 0, 1)  # 买平
        # self.order_insert('CFFEX', 'IF2506', 3880, 2, 0, 1, 1)  # 卖平

    def order_insert(self, exchange_id: str, instrument_id: str, price: float, volume: int = 1, priceType: int = 0, direction: int = 0, offset: int = 0):
        """报单录入请求

        - 录入错误时对应响应OnRspOrderInsert、OnErrRtnOrderInsert，
        - 正确时对应回报OnRtnOrder、OnRtnTrade。
        """
        print(" [限价单]") if priceType == 0 else print(" [市价单]")
        # 市价单, 注意选择一个相对活跃的合约
        # simnow 目前貌似不支持市价单，所以会被自动撤销！！！

        OrderPriceType = tdapi.THOST_FTDC_OPT_LimitPrice if priceType == 0 else tdapi.THOST_FTDC_OPT_AnyPrice   # 价格类型 限价单 市价单
        Direction = tdapi.THOST_FTDC_D_Buy if direction == 0 else tdapi.THOST_FTDC_D_Sell  # 买 卖
        CombOffsetFlag = tdapi.THOST_FTDC_OF_Open if offset == 0 else tdapi.THOST_FTDC_OF_Close  # 开仓 平仓

        # 限价单 注意选择一个相对活跃的合约及合适的价格
        req = tdapi.CThostFtdcInputOrderField()
        req.BrokerID = self._broker_id
        req.InvestorID = self._user_id
        req.ExchangeID = exchange_id
        req.InstrumentID = instrument_id  # 合约ID
        req.LimitPrice = price  # 价格
        req.OrderPriceType = OrderPriceType  # 价格类型
        req.Direction = Direction  # 方向
        req.CombOffsetFlag = CombOffsetFlag  # 开平标志
        req.CombHedgeFlag = tdapi.THOST_FTDC_HF_Speculation
        req.VolumeTotalOriginal = volume
        req.IsAutoSuspend = 0
        req.IsSwapOrder = 0
        req.TimeCondition = tdapi.THOST_FTDC_TC_GFD
        req.VolumeCondition = tdapi.THOST_FTDC_VC_AV
        req.ContingentCondition = tdapi.THOST_FTDC_CC_Immediately
        req.ForceCloseReason = tdapi.THOST_FTDC_FCC_NotForceClose
        self._check_req(req, self._api.ReqOrderInsert(req, 0))

    def OnRspOrderInsert(self, pInputOrder: tdapi.CThostFtdcInputOrderField, pRspInfo: tdapi.CThostFtdcRspInfoField,
                         nRequestID: int, bIsLast: bool):
        """ 报单录入请求响应 """
        self._check_rsp(pRspInfo, pInputOrder, bIsLast)

    def OnRtnOrder(self, pOrder: tdapi.CThostFtdcOrderField):
        """ 报单通知，当执行ReqOrderInsert后并且报出后，收到返回则调用此接口，私有流回报。 """
        self._print_rtn(pOrder, f'报单通知[{pOrder.StatusMsg}]')
        print(f"\tOrderSysID={pOrder.OrderSysID}, FrontID={pOrder.FrontID}, "
              f"SessionID={pOrder.SessionID}, OrderRef={pOrder.OrderRef}")

    def OnRtnTrade(self, pTrade: tdapi.CThostFtdcTradeField):
        """ 成交通知，报单发出后有成交则通过此接口返回。私有流 """
        self._print_rtn(pTrade, "成交通知")

    def OnErrRtnOrderInsert(self, pInputOrder: tdapi.CThostFtdcInputOrderField, pRspInfo: tdapi.CThostFtdcRspInfoField):
        """ 报单录入错误回报 """
        self._print_rtn(pInputOrder, "报单录入错误回报", pRspInfo=pRspInfo)


if __name__ == '__main__':
    spi = CTdSpi()
    spi.req()

    spi.wait_last()
