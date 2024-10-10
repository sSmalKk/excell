const axios = require("axios");

const getReceipts = async () => {
  try {
    const response = await axios.get(
      'https://www.vendus.pt/ws/v1.1/receipts/',
      {
        headers: {
          Authorization: `Bearer 8b0d2332da3f445e46a163c67d8fa7b0`,
        },
        params: {
          status: 'active',
        }
      }
    );
    
    // Handle the response data here
    console.log("Receipts:", response.data);
    
  } catch (error) {
    console.error("Error fetching receipts:", error.response ? error.response.data : error.message);
  }
};

getReceipts();
