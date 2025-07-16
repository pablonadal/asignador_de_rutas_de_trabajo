import React from 'react';
import { StyleSheet, Text, View, Button } from 'react-native';

export default function App() {
  const [message, setMessage] = React.useState('Bienvenido');

  const handlePress = () => {
    // Aquí se podría llamar a una API del backend
    setMessage('Hola desde la app móvil');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Asignador de Rutas</Text>
      <Text>{message}</Text>
      <Button title="Presionar" onPress={handlePress} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
});