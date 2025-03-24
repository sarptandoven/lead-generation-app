import { extendTheme } from '@chakra-ui/react';

const colors = {
  primary: {
    50: '#fff3e6',
    100: '#ffe0cc',
    200: '#ffc299',
    300: '#ffa366',
    400: '#ff8533',
    500: '#ff6600', // Main brand color from Corgi
    600: '#cc5200',
    700: '#993d00',
    800: '#662900',
    900: '#331400',
  },
  secondary: {
    50: '#e6f5ff',
    100: '#b3e0ff',
    200: '#80ccff',
    300: '#4db8ff',
    400: '#1aa3ff',
    500: '#0088ff',
    600: '#006dd1',
    700: '#0052a3',
    800: '#003875',
    900: '#001d47',
  },
  neutral: {
    50: '#f7f7f7',
    100: '#e3e3e3',
    200: '#c8c8c8',
    300: '#a4a4a4',
    400: '#808080',
    500: '#666666',
    600: '#4d4d4d',
    700: '#333333',
    800: '#1a1a1a',
    900: '#0d0d0d',
  },
};

const fonts = {
  heading: 'Inter, -apple-system, system-ui, sans-serif',
  body: 'Inter, -apple-system, system-ui, sans-serif',
};

const components = {
  Button: {
    baseStyle: {
      fontWeight: 600,
      borderRadius: 'md',
    },
    variants: {
      solid: {
        bg: 'primary.500',
        color: 'white',
        _hover: {
          bg: 'primary.600',
        },
      },
      outline: {
        borderColor: 'primary.500',
        color: 'primary.500',
        _hover: {
          bg: 'primary.50',
        },
      },
    },
  },
  Card: {
    baseStyle: {
      container: {
        borderRadius: 'xl',
        boxShadow: 'lg',
      },
    },
  },
  Input: {
    variants: {
      filled: {
        field: {
          bg: 'neutral.50',
          _hover: {
            bg: 'neutral.100',
          },
          _focus: {
            bg: 'white',
            borderColor: 'primary.500',
          },
        },
      },
    },
  },
};

const shadows = {
  outline: '0 0 0 3px rgba(255, 102, 0, 0.2)',
};

const styles = {
  global: {
    body: {
      bg: 'white',
      color: 'neutral.800',
    },
  },
};

export const theme = extendTheme({
  colors,
  fonts,
  components,
  shadows,
  styles,
  config: {
    initialColorMode: 'light',
    useSystemColorMode: false,
  },
}); 