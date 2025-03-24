import React from 'react';
import {
  Box,
  Button,
  Container,
  Flex,
  Heading,
  Icon,
  Image,
  SimpleGrid,
  Stack,
  Text,
  useColorModeValue,
} from '@chakra-ui/react';
import { FaRobot, FaSearchDollar, FaChartLine } from 'react-icons/fa';
import { motion } from 'framer-motion';

const MotionBox = motion(Box);
const MotionFlex = motion(Flex);

const Feature = ({ title, text, icon }: { title: string; text: string; icon: React.ElementType }) => {
  return (
    <Stack spacing={4} align="center" textAlign="center">
      <Flex
        w={16}
        h={16}
        align="center"
        justify="center"
        color="white"
        rounded="full"
        bg="primary.500"
        mb={1}
      >
        <Icon as={icon} w={8} h={8} />
      </Flex>
      <Text fontWeight={600} fontSize="lg">
        {title}
      </Text>
      <Text color="gray.600">{text}</Text>
    </Stack>
  );
};

const LandingPage = () => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const textColor = useColorModeValue('gray.600', 'gray.200');

  return (
    <Box bg={bgColor}>
      {/* Hero Section */}
      <Container maxW="container.xl" pt={{ base: 20, md: 28 }} pb={20}>
        <Stack spacing={8} align="center" textAlign="center">
          <MotionBox
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Heading
              as="h1"
              size="2xl"
              fontWeight={800}
              mb={4}
              bgGradient="linear(to-r, primary.500, secondary.500)"
              bgClip="text"
            >
              Intelligent Lead Generation
              <br />
              Powered by AI
            </Heading>
          </MotionBox>
          <Text fontSize="xl" color={textColor} maxW="2xl">
            Transform your business with our advanced AI-powered lead generation platform.
            Discover high-quality leads, automate outreach, and scale your growth.
          </Text>
          <Stack direction={{ base: 'column', sm: 'row' }} spacing={4}>
            <Button
              size="lg"
              colorScheme="primary"
              px={8}
              fontSize="md"
              height="14"
              as={motion.button}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Get Started
            </Button>
            <Button
              size="lg"
              variant="outline"
              px={8}
              fontSize="md"
              height="14"
              as={motion.button}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Watch Demo
            </Button>
          </Stack>
        </Stack>

        {/* Feature Section */}
        <Box mt={20}>
          <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10}>
            <Feature
              icon={FaRobot}
              title="AI-Powered Intelligence"
              text="Our advanced AI algorithms analyze millions of data points to identify your ideal prospects."
            />
            <Feature
              icon={FaSearchDollar}
              title="Smart Lead Scoring"
              text="Automatically score and prioritize leads based on their likelihood to convert."
            />
            <Feature
              icon={FaChartLine}
              title="Advanced Analytics"
              text="Get deep insights into your lead generation performance with real-time analytics."
            />
          </SimpleGrid>
        </Box>

        {/* Integration Section */}
        <MotionFlex
          mt={20}
          direction={{ base: 'column', md: 'row' }}
          align="center"
          justify="space-between"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Box flex={1} mr={{ base: 0, md: 8 }} mb={{ base: 8, md: 0 }}>
            <Heading size="lg" mb={4}>
              Seamless Integration
            </Heading>
            <Text color={textColor} fontSize="lg">
              Connect with your favorite tools and automate your entire lead generation workflow.
              Our platform integrates with leading CRM systems, email marketing tools, and more.
            </Text>
            <Button
              mt={6}
              size="lg"
              variant="link"
              colorScheme="primary"
              rightIcon={<Icon as={FaChartLine} />}
            >
              View All Integrations
            </Button>
          </Box>
          <Box flex={1}>
            <Image
              src="/integration-diagram.svg"
              alt="Integration Diagram"
              w="full"
              h="auto"
              rounded="lg"
              shadow="2xl"
            />
          </Box>
        </MotionFlex>
      </Container>
    </Box>
  );
};

export default LandingPage; 