import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import {
    Box,
    Button,
    Text,
    VStack,
    useToast,
    Alert,
    AlertIcon,
    AlertTitle,
    AlertDescription,
    Badge,
    Spinner,
} from '@chakra-ui/react';

const DigestView = () => {
    const [digest, setDigest] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const toast = useToast();

    const generateDigest = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch('http://localhost:8000/api/digest/generate');
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || 'Failed to generate digest');
            }
            
            setDigest(data);
            toast({
                title: 'Digest Generated',
                description: `Generated ${data.story_count} stories with minimum score ${data.min_score}`,
                status: 'success',
                duration: 5000,
                isClosable: true,
            });
        } catch (err) {
            setError(err.message);
            toast({
                title: 'Error',
                description: err.message,
                status: 'error',
                duration: 5000,
                isClosable: true,
            });
        } finally {
            setLoading(false);
        }
    };

    const downloadDigest = () => {
        if (!digest) return;
        
        const blob = new Blob([digest.content], { type: 'text/markdown' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ai-news-digest-${new Date().toISOString().split('T')[0]}.md`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    };

    return (
        <Box>
            <Box mb={6} display="flex" alignItems="center" gap={4}>
                <Button
                    colorScheme="blue"
                    onClick={generateDigest}
                    isLoading={loading}
                    loadingText="Generating..."
                >
                    Generate Daily Digest
                </Button>
                {digest && (
                    <Button
                        colorScheme="green"
                        onClick={downloadDigest}
                    >
                        Download Markdown
                    </Button>
                )}
            </Box>

            {error && (
                <Alert status="error" mb={4}>
                    <AlertIcon />
                    <AlertTitle>Error!</AlertTitle>
                    <AlertDescription>{error}</AlertDescription>
                </Alert>
            )}

            {digest && (
                <VStack spacing={4} align="stretch">
                    <Box p={4} bg="gray.50" borderRadius="md">
                        <Text>
                            Generated at: {new Date(digest.generated_at).toLocaleString()}
                        </Text>
                        <Box mt={2} display="flex" gap={2}>
                            <Badge colorScheme="purple">
                                Stories: {digest.story_count}
                            </Badge>
                            <Badge colorScheme="green">
                                Min Score: {digest.min_score}
                            </Badge>
                        </Box>
                    </Box>

                    <Box
                        p={6}
                        bg="white"
                        shadow="md"
                        borderRadius="md"
                        className="markdown-content"
                    >
                        <ReactMarkdown>{digest.content}</ReactMarkdown>
                    </Box>
                </VStack>
            )}

            {loading && (
                <Box textAlign="center" my={8}>
                    <Spinner size="xl" />
                    <Text mt={4}>Generating digest...</Text>
                </Box>
            )}
        </Box>
    );
};

export default DigestView;