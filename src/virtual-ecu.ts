/**
 * VirtualECU - FMU (Functional Mock-up Unit) Implementation
 * 
 * This virtual ECU demonstrates a simple arithmetic unit with metadata
 * that can be queried through the MCP server interface.
 */

export interface ECUMetadata {
  software: string;
  version: string;
  interfaces: string[];
  level: string;
  description: string;
  domain: string;
}

export interface ECUFunction {
  name: string;
  description: string;
  parameters: { name: string; type: string; description: string }[];
  returnType: string;
}

export class VirtualECU {
  private metadata: ECUMetadata;
  private functions: ECUFunction[];

  constructor() {
    this.metadata = {
      software: "Virtual ECU Addition Unit",
      version: "1.0.0",
      interfaces: ["addition", "metadata", "status"],
      level: "L2 - Basic Arithmetic Functions",
      description: "A virtual ECU FMU that provides basic addition functionality and queryable metadata",
      domain: "Automotive - Basic Arithmetic Control Unit"
    };

    this.functions = [
      {
        name: "add",
        description: "Perform addition operation on two numbers",
        parameters: [
          { name: "a", type: "number", description: "First number to add" },
          { name: "b", type: "number", description: "Second number to add" }
        ],
        returnType: "number"
      },
      {
        name: "getMetadata",
        description: "Get complete metadata about the Virtual ECU including software, version, interfaces, level, and domain",
        parameters: [],
        returnType: "ECUMetadata"
      },
      {
        name: "getSoftware",
        description: "Get the software name of the Virtual ECU",
        parameters: [],
        returnType: "string"
      },
      {
        name: "getVersion",
        description: "Get the version number of the Virtual ECU",
        parameters: [],
        returnType: "string"
      },
      {
        name: "getInterfaces",
        description: "Get the list of available interfaces in the Virtual ECU",
        parameters: [],
        returnType: "string[]"
      },
      {
        name: "getLevel",
        description: "Get the capability level of the Virtual ECU",
        parameters: [],
        returnType: "string"
      },
      {
        name: "getStatus",
        description: "Get the current operational status of the Virtual ECU",
        parameters: [],
        returnType: "string"
      },
      {
        name: "getDomain",
        description: "Get the domain/application area of the Virtual ECU",
        parameters: [],
        returnType: "string"
      },
      {
        name: "listFunctions",
        description: "List all available functions in the Virtual ECU with their descriptions and signatures",
        parameters: [],
        returnType: "ECUFunction[]"
      }
    ];
  }

  /**
   * Perform addition operation (core FMU functionality)
   */
  add(a: number, b: number): number {
    return a + b;
  }

  /**
   * Get ECU metadata
   */
  getMetadata(): ECUMetadata {
    return { ...this.metadata };
  }

  /**
   * Get software information
   */
  getSoftware(): string {
    return this.metadata.software;
  }

  /**
   * Get version information
   */
  getVersion(): string {
    return this.metadata.version;
  }

  /**
   * Get available interfaces
   */
  getInterfaces(): string[] {
    return [...this.metadata.interfaces];
  }

  /**
   * Get ECU level
   */
  getLevel(): string {
    return this.metadata.level;
  }

  /**
   * Get current status of the ECU
   */
  getStatus(): string {
    return "ECU is operational and ready";
  }

  /**
   * Get ECU domain/application area
   */
  getDomain(): string {
    return this.metadata.domain;
  }

  /**
   * List all available functions in the ECU
   */
  listFunctions(): ECUFunction[] {
    return [...this.functions];
  }
}
