import React from 'react';
import Progress from './Progress';

const HEADERS = ["r1", "r2", "r3", "s1", "s2", "s3", "pivot_points"];

function Technicals({ data }) {
  return (
    <div className="segment">
        <Progress
            title="Bullish"
            color="#21ba45"
            percentage={data.percent_bullish} />
        <Progress
            title="Bearish"
            color="#db2828"
            percentage={data.percent_bearish} />
        <table>
            <thead>
            <tr>
                {HEADERS.map((item) => (
                <th key={item}>{item.toUpperCase()}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          <tr>
            {HEADERS.map((item) => (
              <td key={item}>{data[item]}</td>
            ))}
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Technicals;
