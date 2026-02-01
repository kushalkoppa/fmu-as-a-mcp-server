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
}

export class VirtualECU {
  private metadata: ECUMetadata;

  constructor() {
    this.metadata = {
      software: "Virtual ECU Addition Unit",
      version: "1.0.0",
      interfaces: ["addition", "metadata", "status"],
      level: "L2 - Basic Arithmetic Functions",
      description: "A virtual ECU FMU that provides basic addition functionality and queryable metadata"
    };
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
}
