import React, { useState, useEffect } from 'react';
import {
  ChakraProvider,
  Box,
  Container,
  Heading,
  Text,
  VStack,
  Link,
  Badge,
  Spinner,
  useToast,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from '@chakra-ui/react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

function App() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const toast = useToast();

  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = async () => {
    try {
      console.log('Fetching news from:', `${API_URL}/api/news`);
      const response = await axios.get(`${API_URL}/api/news`);
      console.log('API Response:', response.data);
      setNews(response.data);
      setError(null);
    } catch (error) {
      console.error('Error details:', error);
      setError(error.response?.data?.error || error.message);
      toast({
        title: 'Error fetching news',
        description: error.response?.data?.error || error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <ChakraProvider>
      <Box bg="gray.50" minH="100vh" py={8}>
        <Container maxW="container.lg">
          <Heading mb={8} textAlign="center">AI News Aggregator</Heading>
          
          {error && (
            <Alert status="error" mb={4}>
              <AlertIcon />
              <AlertTitle>Error!</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {loading ? (
            <Box textAlign="center">
              <Spinner size="xl" />
              <Text mt={4}>Loading news...</Text>
            </Box>
          ) : (
            <VStack spacing={4} align="stretch">
              {news.length === 0 && !error ? (
                <Alert status="info">
                  <AlertIcon />
                  No news articles found
                </Alert>
              ) : (
                news.map((item, index) => (
                  <Box
                    key={index}
                    p={5}
                    shadow="md"
                    borderWidth="1px"
                    borderRadius="md"
                    bg="white"
                  >
                    <Heading size="md" mb={2}>
                      <Link href={item.url} isExternal color="blue.600">
                        {item.title}
                      </Link>
                    </Heading>
                    <Text color="gray.600" mb={3}>
                      {item.description}
                    </Text>
                    <Box display="flex" alignItems="center" gap={2}>
                      <Badge colorScheme="purple">
                        {item.source}
                      </Badge>
                      <Badge colorScheme="green">
                        Score: {item.interesting_score.toFixed(2)}
                      </Badge>
                    </Box>
                  </Box>
                ))
              )}
            </VStack>
          )}
        </Container>
      </Box>
    </ChakraProvider>
  );
}

export default App;