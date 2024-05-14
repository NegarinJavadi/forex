import React, { useEffect, useState } from 'react'
import TitleHead from './TitleHead'

const DATA_KEYS = [
  {name: "Account Num.", key:"id", fixed: -1}, 
  {name: "balance", key:"balance", fixed: -1}, 
  {name: "NAV", key:"nav", fixed: -1}, 
  {name: "Open Trades", key:"openTradeCount", fixed: -1}, 
  {name: "Unrealized PL", key:"unrealizedPL", fixed: -1}, 
  {name: "Closeout %", key:"marginCloseoutPercent", fixed: -1},
  {name: "Last Trans. ID", key:"lastTransactionID", fixed: -1},  
]

function AccountSummary() {

  const[account, setAccount] = useState(null);

  useEffect(() =>{
    loadAccount();
  }, [])

  const loadAccount = async() => {
    const data = await endPoints.account();
    setAccount(data);
  }
  return (
    <div>
        <TitleHead title="Account Summary" />
        {
          account && <div>
            <pre>{JSON.stringify(account, null, 2)}</pre>
            
          </div>
        }
    </div>
  )
}

export default AccountSummary