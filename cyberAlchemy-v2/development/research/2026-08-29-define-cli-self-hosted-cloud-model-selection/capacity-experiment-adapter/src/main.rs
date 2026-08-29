use capacity_experiment_adapter::{adapt_run, materialize_scenario_runs, validate_run, Error};
use clap::{Parser, Subcommand};
use std::path::PathBuf;

#[derive(Parser)]
#[command(
    name = "capacity-experiment",
    about = "Convert raw serving and swarm runs into capacity-curve profiles"
)]
struct Cli {
    #[command(subcommand)]
    command: Command,
}
#[derive(Subcommand)]
enum Command {
    Validate {
        #[arg(long)]
        run_dir: PathBuf,
    },
    Adapt {
        #[arg(long)]
        run_dir: PathBuf,
        #[arg(long)]
        out_dir: PathBuf,
    },
    Scenario {
        #[arg(long)]
        policy: PathBuf,
        #[arg(long, required = true)]
        run_dir: Vec<PathBuf>,
        #[arg(long)]
        out_dir: PathBuf,
    },
}
fn run() -> capacity_experiment_adapter::Result<()> {
    match Cli::parse().command {
        Command::Validate { run_dir } => {
            validate_run(&run_dir)?;
            println!("valid {}", run_dir.display());
        }
        Command::Adapt { run_dir, out_dir } => {
            let result = adapt_run(&run_dir, &out_dir)?;
            println!("adapted {} -> {}", result.receipt.run_id, out_dir.display());
        }
        Command::Scenario {
            policy,
            run_dir,
            out_dir,
        } => {
            let scenario = materialize_scenario_runs(&policy, &run_dir, &out_dir)?;
            println!("materialized {}", scenario.display());
        }
    }
    Ok(())
}
fn main() {
    if let Err(error) = run() {
        eprintln!("error: {error}");
        std::process::exit(match error {
            Error::Invalid(_) | Error::Json(_) | Error::Core(_) => 2,
            Error::Io(_) => 3,
        })
    }
}
