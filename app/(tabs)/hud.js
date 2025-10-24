// app/(tabs)/hud.js (Partial update - add imports/constant)
import Constants from 'expo-constants'; // <--- NEW IMPORT
import axios from 'axios';            // <--- NEW IMPORT

// ... (existing code)

export default function HUD() {
  // ... (existing useState and useSharedValue)

  const store = useStore(); 
  
  // Retrieve the global backend URL
  const backendUrl = Constants.expoConfig.extra.backendUrl; // <--- NEW CONSTANT

  useEffect(() => {
    // ... (existing sensor setup code)
    // ...
  }, []);

  // NEW: Function to trigger the IBM task via the Termux server
  const runIBMJob = async () => {
      store.setIBMStatus('Triggering IBM Job...');
      try {
        // Use the global variable here
        const response = await axios.get(`${backendUrl}/run_ibm`); 
        store.setIBMStatus(`Job started: ${response.data.status}`);
      } catch (error) {
        store.setIBMStatus('Request Failed: Check Termux Server/IP');
        console.error("IBM Trigger Error:", error.message);
      }
  };

  return (
    <View style={styles.container}>
      {/* ... (existing HUD components) */}
      <Text style={styles.text}>IBM Validation: {store.ibmStatus || 'Pending'}</Text>
      <Button title="Trigger IBM Validation" onPress={runIBMJob} /> {/* <--- NEW BUTTON */}
    </View>
  );
}
