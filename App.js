import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Button, Alert } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import * as Location from 'expo-location';
import * as Sensors from 'expo-sensors';
import { Camera } from 'expo-camera';
import Reanimated, { useSharedValue, useAnimatedStyle, withRepeat, withTiming } from 'react-native-reanimated';
import LottieView from 'lottie-react-native';
import axios from 'axios';

const BACKEND_URL = 'http://localhost:8080'; // Or your server IP for Termux

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#1a1a1a', alignItems: 'center', justifyContent: 'center' },
  text: { color: '#ffd700', fontFamily: 'serif', fontSize: 18 },
  gear: { width: 150, height: 150 }
});

// ESQET FQC in JS (with observer)
const PHI = (1 + Math.sqrt(5)) / 2;
const PI = Math.PI;
const ALPHA_DARK = 0.4;
const I_0 = 1e-34;
const K_B = 1.380649e-23;
function computeFQC(dent = 1e-10, tvac = 1e-10, delta = 0.5, scale = 1, dent_obs = 0.1, phi_obs = 0) {
  const fcu = PHI * PI * delta;
  const term1 = 1 + fcu * (dent + dent_obs) * I_0 / (K_B * Math.max(tvac, 1e-30));
  const term2 = 1 + ALPHA_DARK * (0.9e-26 / 1e-26);
  const term3 = 1 + Math.cos(2 * PHI * PI / scale + phi_obs);
  return term1 * term2 * term3;
}

// Virtual Quantum Build Sim
function virtualQuantumSim() {
  const qc = { qubits: 2, state: [Math.sqrt(0.5), 0, 0, Math.sqrt(0.5)] }; // Bell
  return { counts: { '00': 512, '11': 512 } };
}

// Virtual Blockchain Build Sim
class Block {
  constructor(index, prevHash, data) {
    this.index = index;
    this.prevHash = prevHash;
    this.data = data;
    this.hash = require('crypto-js/sha256')(JSON.stringify(this)).toString();
  }
}
function virtualBlockchain() {
  const chain = [];
  chain.push(new Block(0, '0', 'ESQET Genesis'));
  chain.push(new Block(1, chain[0].hash, 'Oracle Data'));
  return chain.map(b => b.hash);
}

// HUD Screen
function HUDScreen() {
  const [fqc, setFQC] = useState(0);
  const [state, setState] = useState({ heading: 0, accel: 0 });
  const rotation = useSharedValue(0);
  useEffect(() => {
    rotation.value = withRepeat(withTiming(360, { duration: 2000 }), -1);
    (async () => {
      await Location.requestForegroundPermissionsAsync();
      await Camera.requestCameraPermissionsAsync();
      Sensors.Accelerometer.addListener(({ x, y, z }) => setState(s => ({ ...s, accel: Math.sqrt(x**2 + y**2 + z**2) })));
      const loc = await Location.getCurrentPositionAsync();
      setState(s => ({ ...s, heading: loc.coords.heading }));
      setFQC(computeFQC(1e-10, 1e-10, 0.5, 1, 0.1, loc.coords.heading / 180 * PI)); // Observer from heading
    })();
  }, []);

  const animatedStyle = useAnimatedStyle(() => ({ transform: [{ rotate: `${rotation.value}deg` }] }));

  const mintNFT = async () => {
    try {
      const res = await axios.post(`${BACKEND_URL}/generate_nft/`, { prompt: 'ESQET Oracle Egg', series: 'Eggs', use_ibm: false, creator_address: '0xYourAddr' });
      Alert.alert('Minted!', `IPFS: ${res.data.ipfs}, TX: ${res.data.tx_hash}`);
    } catch (e) {
      Alert.alert('Error', e.message);
    }
  };

  const callOracle = async () => {
    try {
      const res = await axios.post(`${BACKEND_URL}/oracle/evolve`);
      Alert.alert('Oracle Proposal', res.data.proposal);
    } catch (e) {
      Alert.alert('Error', e.message);
    }
  };

  return (
    <View style={styles.container}>
      <Reanimated.View style={[styles.gear, animatedStyle]}>
        <LottieView source={require('./assets/gear.json')} autoPlay loop />
      </Reanimated.View>
      <Text style={styles.text}>FQC: {fqc.toFixed(2)}</Text>
      <Text style={styles.text}>Heading: {state.heading}° | Accel: {state.accel.toFixed(1)}</Text>
      <Text style={styles.text}>Quantum Sim: {JSON.stringify(virtualQuantumSim().counts)}</Text>
      <Text style={styles.text}>Blockchain Sim: {JSON.stringify(virtualBlockchain())}</Text>
      <Button title="Mint QH-NFT" onPress={mintNFT} />
      <Button title="Consult Oracle (Propose Update)" onPress={callOracle} />
    </View>
  );
}

const Stack = createStackNavigator();
export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Oracle HUD" component={HUDScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
