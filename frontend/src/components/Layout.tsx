import React from 'react';
import {
  Box,
  Container,
  Stack,
  StackProps,
  Flex,
  FlexProps,
  HStack,
  IconButton,
  useColorModeValue,
  Image,
  Button,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
} from '@chakra-ui/react';
import { HamburgerIcon, ChevronDownIcon } from '@chakra-ui/icons';
import { Link as RouterLink } from 'react-router-dom';

interface LayoutProps {
  children: React.ReactNode;
}

const Navigation = () => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.100', 'gray.700');

  return (
    <Box
      as="nav"
      position="fixed"
      w="100%"
      bg={bgColor}
      borderBottom="1px"
      borderColor={borderColor}
      zIndex="sticky"
    >
      <Container maxW="container.xl">
        <Flex h="16" alignItems="center" justify="space-between">
          <HStack spacing={8} alignItems="center">
            <Box as={RouterLink} to="/" _hover={{ opacity: 0.8 }}>
              <Image h="32px" src="/logo.svg" alt="Logo" />
            </Box>
            <HStack spacing={4} display={{ base: 'none', md: 'flex' }}>
              <Menu>
                <MenuButton
                  as={Button}
                  variant="ghost"
                  rightIcon={<ChevronDownIcon />}
                >
                  Features
                </MenuButton>
                <MenuList>
                  <MenuItem as={RouterLink} to="/lead-generation">Lead Generation</MenuItem>
                  <MenuItem as={RouterLink} to="/analytics">Analytics</MenuItem>
                  <MenuItem as={RouterLink} to="/automation">Automation</MenuItem>
                </MenuList>
              </Menu>
              <Button as={RouterLink} to="/pricing" variant="ghost">
                Pricing
              </Button>
              <Button as={RouterLink} to="/about" variant="ghost">
                About
              </Button>
            </HStack>
          </HStack>

          <HStack spacing={4}>
            <Button
              as={RouterLink}
              to="/dashboard"
              colorScheme="primary"
              display={{ base: 'none', md: 'inline-flex' }}
            >
              Dashboard
            </Button>
            <IconButton
              display={{ base: 'flex', md: 'none' }}
              aria-label="Open menu"
              icon={<HamburgerIcon />}
              variant="ghost"
            />
          </HStack>
        </Flex>
      </Container>
    </Box>
  );
};

const Footer = () => {
  const borderColor = useColorModeValue('gray.100', 'gray.700');

  return (
    <Box
      as="footer"
      borderTop="1px"
      borderColor={borderColor}
      py={8}
      mt="auto"
    >
      <Container maxW="container.xl">
        <Stack
          direction={{ base: 'column', md: 'row' }}
          justify="space-between"
          align="center"
          spacing={4}
        >
          <Box>
            <Image h="24px" src="/logo.svg" alt="Logo" mb={2} />
            <Box color="gray.500" fontSize="sm">
              © {new Date().getFullYear()} All rights reserved.
            </Box>
          </Box>
          <HStack spacing={8} mt={{ base: 4, md: 0 }}>
            <Button as={RouterLink} to="/privacy" variant="link" size="sm">
              Privacy Policy
            </Button>
            <Button as={RouterLink} to="/terms" variant="link" size="sm">
              Terms of Service
            </Button>
            <Button as={RouterLink} to="/contact" variant="link" size="sm">
              Contact
            </Button>
          </HStack>
        </Stack>
      </Container>
    </Box>
  );
};

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const bgColor = useColorModeValue('gray.50', 'gray.900');

  return (
    <Flex direction="column" minH="100vh" bg={bgColor}>
      <Navigation />
      <Box as="main" flex={1} pt="16">
        <Container maxW="container.xl" py={8}>
          {children}
        </Container>
      </Box>
      <Footer />
    </Flex>
  );
};

export default Layout; 