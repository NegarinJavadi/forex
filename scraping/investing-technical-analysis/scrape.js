const axios = require('axios');

async function investingComFetch(pairID, timeFrame) {
  try {
    const response = await axios.post('https://www.investing.com/technical/Service/GetStudiesContent', 
      `action=get_studies&pair_ID=${pairID}&time_frame=${timeFrame}`, {
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0'
      },
      timeout: 10000  // Increase timeout to 10 seconds
    });

    // Check if data indices exist in response
    if (!response.data || !response.data.someExpectedField) {
      console.error('Data indices not found in the response text.');
      return;
    }

    // Process the data as required
    console.log('Data fetched successfully', response.data);
  } catch (error) {
    if (error.code === 'ETIMEDOUT' || error.code === 'ENETUNREACH') {
      console.error(`Network error: ${error.code}. Address: ${error.address}. Port: ${error.port}`);
    } else {
      console.error('Error fetching data:', error);
    }
  }
}

async function investingCom() {
  const pairs = [1, 2, 3, 4, 5, 6];
  const timeFrames = [3600, 86400];

  for (const pair of pairs) {
    for (const timeFrame of timeFrames) {
      await investingComFetch(pair, timeFrame);
    }
  }
}

investingCom();
