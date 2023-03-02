-- Create the database
CREATE DATABASE MyDW
ON PRIMARY 
   (NAME = MyDWData, FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\MyDWData.mdf', SIZE = 512MB, MAXSIZE = 1GB, FILEGROWTH = 128MB)
LOG ON 
   (NAME = MyDWLog, FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\Log\MyDWData.ldf', SIZE = 256MB, MAXSIZE = 500MB, FILEGROWTH = 64MB);

-- Create the filegroup
ALTER DATABASE MyDW ADD FILEGROUP MyDWFG1;

-- Create the data files on the filegroup
ALTER DATABASE MyDW ADD FILE (NAME = MyDWFG1Data1, FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\Data\MyDWFG1.ndf', SIZE = 512MB, MAXSIZE = 1024MB, FILEGROWTH = 64MB) TO FILEGROUP MyDWFG1;
ALTER DATABASE MyDW ADD FILE (NAME = MyDWFG1Data2, FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\Data\MyDWFG2.ndf', SIZE = 512MB, MAXSIZE = 1024MB, FILEGROWTH = 64MB) TO FILEGROUP MyDWFG1;

-- Set the default schema
USE MyDW
go
create schema [crypto]
go


-- Create the CoinDimension table 
CREATE TABLE crypto.DimCoin (
   	[ID] [smallint] IDENTITY(1,1) NOT NULL,
	[CoinID] [int] NOT NULL,
	[Name] [varchar](100) NOT NULL,
	[Symbol] [varchar](10) NOT NULL,
 CONSTRAINT [PK_DimCoin] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)with(data_compression=page,PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [MyDWFG1],
    CONSTRAINT UC_DimCoin_Name_Symbol UNIQUE (Name, Symbol)
) ON MyDWFG1 
with(data_compression=page);

--Create the DateDimension table 
CREATE TABLE crypto.DimDate (
   [DateID] [int] NOT NULL,
	[Year] [int] NOT NULL,
	[Quarter] [int] NOT NULL,
	[Month] [int] NOT NULL,
	[Day] [int] NOT NULL,
 CONSTRAINT [PK__DimDate__02EA064FDC461E74] PRIMARY KEY CLUSTERED 
(
	[DateID] ASC
)WITH (data_compression=page,PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [MyDWFG1]
) ON [MyDWFG1]
with(data_compression=page);



--create FactPrice
CREATE TABLE [crypto].[FactPrice](
    [PriceId] [bigint] IDENTITY(1,1) NOT NULL,
	[CoinId] [int] NOT NULL,
	[Date] [int] NOT NULL,
	[OpenPrice] [float] NOT NULL,
	[ClosePrice] [float] NOT NULL,
	[HighPrice] [float] NOT NULL,
	[LowPrice] [float] NOT NULL,
	[Volume] [float] NOT NULL,
	[MarketCap] [float] NOT NULL,
 CONSTRAINT [PK_FactPrice] PRIMARY KEY CLUSTERED 
(
	[PriceId] ASC
)WITH (data_compression=page,PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [MyDWFG1]
)ON MyDWFG1 
with(data_compression=page);



